#include <stdlib.h>
#include <math.h>
#ifdef _OPENMP
#include <omp.h>
#endif

#include "wildfire_parallel.h"
#include "wildfire.h"   /* reuse sequential helpers */

/* Thread-safe wrapper around add_fire_source using OpenMP critical section. */
static void add_fire_source_threadsafe(FireSystem *fs, const FireSource *src)
{
#ifdef _OPENMP
#pragma omp critical(add_fire)
#endif
    {
        unsigned new_count = fs->source_count + 1;
        FireSource *tmp = (FireSource*)realloc(fs->sources,
                                               new_count * sizeof(FireSource));
        if (!tmp)
            return;
        fs->sources = tmp;
        fs->sources[new_count - 1] = *src;
        fs->source_count = new_count;
    }
}

/* ------------------------------------------------------------------------- */
/*  Weather-aware evolve & spread variants (parallel)                        */
/* ------------------------------------------------------------------------- */

static void evolve_parallel(FireSystem *fs, float dt, const Weather *w)
{
    const float base_burn_rate = 0.08f; /* kg/s at intensity 1 */
#ifdef _OPENMP
#pragma omp parallel for schedule(static)
#endif
    for (unsigned i = 0; i < fs->source_count; ++i) {
        FireSource *src = &fs->sources[i];
        if (!src->is_active)
            continue;

        /* Humidity and precipitation reduce burn rate */
        float damp_factor = 1.0f - fminf(1.0f, w->humidity + w->precipitation_mmph * 0.01f);
        float burn_rate  = base_burn_rate * damp_factor;
        float burn_kg    = burn_rate * src->intensity * dt;
        if (burn_kg > src->fuel_kg)
            burn_kg = src->fuel_kg;
        src->fuel_kg -= burn_kg;

        if (src->fuel_kg > 0.0f) {
            src->intensity = fminf(1.0f, src->fuel_kg / 10.0f);
            src->temperature = 200.0f + src->intensity * 800.0f;
        } else {
            src->is_active   = 0;
            src->intensity   = 0.0f;
            src->temperature = w->temperature;
        }
    }
}

static void spread_parallel(const Mountain *mount, FireSystem *fs, float dt,
                            const Weather *w)
{
    /* constants */
    const float base_prob        = 0.15f;
    const float max_offset_m     = 6.0f;
    const int   attempts_per_src = 3;

    unsigned initial_sources = fs->source_count;

#ifdef _OPENMP
#pragma omp parallel for schedule(static)
#endif
    for (unsigned idx = 0; idx < initial_sources; ++idx) {
        FireSource *src = &fs->sources[idx];
        if (!src->is_active)
            continue;

        float humidity_factor = 1.0f - w->humidity;
        float prob = base_prob * mount->vegetation_density * src->intensity * dt * humidity_factor;
        prob = fminf(prob, 0.9f);

        for (int a = 0; a < attempts_per_src; ++a) {
            float r = rand() / (float)RAND_MAX;
            if (r < prob) {
                float angle = r * 2.0f * (float)M_PI;
                float dist  = (0.5f + r * 0.5f) * max_offset_m;

                Vec3 offset = {
                    cosf(angle) * dist + w->wind_direction.x * w->wind_speed * 0.2f,
                    sinf(angle) * dist + w->wind_direction.y * w->wind_speed * 0.2f,
                    0.0f
                };

                FireSource new_src = *src;
                new_src.position.x += offset.x;
                new_src.position.y += offset.y;
                new_src.radius      = fmaxf(0.5f, src->radius * 0.6f);
                new_src.intensity   = fminf(1.0f, src->intensity * 0.8f + 0.2f);
                new_src.fuel_kg     = 8.0f * mount->vegetation_density + 4.0f;
                new_src.is_active   = 1;

                add_fire_source_threadsafe(fs, &new_src);
            }
        }
    }
}

unsigned wildfire_step_parallel(const Mountain *mount,
                                FireSystem      *fireSys,
                                const WaterSystem *waterSys,
                                const Weather   *weather,
                                float            dt,
                                int              threads)
{
    if (!fireSys || !weather || dt <= 0.0f)
        return 0;

#ifdef _OPENMP
    if (threads > 0)
        omp_set_num_threads(threads);
#endif

    /* Update wind in firesys from weather */
    fireSys->wind_speed     = weather->wind_speed;
    fireSys->wind_direction = weather->wind_direction;

    /* 1. evolve */
    evolve_parallel(fireSys, dt, weather);

    /* 2. external extinguish (water + rain) */
    if (waterSys)
        extinguish_fire_with_water(fireSys, waterSys);

    /* Precipitation auto-extinguish: heavy rain weakens fires */
#ifdef _OPENMP
#pragma omp parallel for schedule(static)
#endif
    for (unsigned i = 0; i < fireSys->source_count; ++i) {
        FireSource *src = &fireSys->sources[i];
        if (!src->is_active)
            continue;
        float rain_factor = weather->precipitation_mmph * 0.02f; /* arbitrary */
        if (rain_factor > 0.0f) {
            src->intensity *= fmaxf(0.0f, 1.0f - rain_factor * dt);
            if (src->intensity < 0.1f) {
                src->is_active = 0;
                src->fuel_kg   = 0.0f;
            }
        }
    }

    /* 3. spread */
    if (mount)
        spread_parallel(mount, fireSys, dt, weather);

    return fireSys->source_count;
}