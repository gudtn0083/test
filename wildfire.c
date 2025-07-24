#include <stdlib.h>  /* rand, RAND_MAX */
#include <math.h>
#include "wildfire.h"

/*----------------------------------------------------------------------*/
/*  Internal helpers                                                    */
/*----------------------------------------------------------------------*/

static float rand_unit(void) {
    return rand() / (float)RAND_MAX; /* [0,1] */
}

static void add_fire_source(FireSystem *fireSys, const FireSource *src)
{
    if (!fireSys || !src) return;

    unsigned new_count = fireSys->source_count + 1;
    FireSource *tmp = (FireSource*)realloc(fireSys->sources,
                                           new_count * sizeof(FireSource));
    if (!tmp)
        return; /* Allocation failed: silently skip */

    fireSys->sources = tmp;
    fireSys->sources[new_count - 1] = *src;
    fireSys->source_count = new_count;
}

/*----------------------------------------------------------------------*/
/*  Public functions                                                    */
/*----------------------------------------------------------------------*/

void wildfire_spread(const Mountain *mount, FireSystem *fireSys, float dt)
{
    if (!mount || !fireSys || dt <= 0.0f)
        return;

    /* Basic constants controlling spread behaviour */
    const float base_prob        = 0.15f; /* base probability per second */
    const float max_offset_m     = 6.0f;  /* maximum radial spread (m)   */
    const int   attempts_per_src = 3;     /* tries per active fire       */

    unsigned initial_sources = fireSys->source_count;

    for (unsigned i = 0; i < initial_sources; ++i) {
        FireSource *src = &fireSys->sources[i];
        if (!src->is_active)
            continue;

        /* Probability scaled by mountain vegetation, fire intensity, time */
        float prob = base_prob * mount->vegetation_density * src->intensity * dt;
        prob = fminf(prob, 0.9f); /* clamp for stability */

        for (int a = 0; a < attempts_per_src; ++a) {
            if (rand_unit() < prob) {
                /* Generate new fire position */
                float angle = rand_unit() * 2.0f * (float)M_PI;
                float dist  = (0.5f + rand_unit() * 0.5f) * max_offset_m; /* 0.5~6 m */

                Vec3 offset = {
                    cosf(angle) * dist + fireSys->wind_direction.x * fireSys->wind_speed * 0.2f,
                    sinf(angle) * dist + fireSys->wind_direction.y * fireSys->wind_speed * 0.2f,
                    0.0f /* assume ground plane */
                };

                FireSource new_src = *src; /* copy seed values */
                new_src.position.x += offset.x;
                new_src.position.y += offset.y;
                new_src.position.z += offset.z;
                new_src.radius      = fmaxf(0.5f, src->radius * 0.6f);
                new_src.intensity   = fminf(1.0f, src->intensity * 0.8f + 0.2f);
                new_src.fuel_kg     = 8.0f * mount->vegetation_density + 4.0f;
                new_src.is_active   = 1;

                add_fire_source(fireSys, &new_src);
            }
        }
    }
}

void wildfire_evolve(FireSystem *fireSys, float dt)
{
    if (!fireSys || dt <= 0.0f)
        return;

    /* Parameters controlling burn behaviour */
    const float burn_rate_coef = 0.08f; /* kg per second at intensity 1 */

    for (unsigned i = 0; i < fireSys->source_count; ++i) {
        FireSource *src = &fireSys->sources[i];
        if (!src->is_active)
            continue;

        float burn_kg = burn_rate_coef * src->intensity * dt;
        if (burn_kg > src->fuel_kg)
            burn_kg = src->fuel_kg;
        src->fuel_kg -= burn_kg;

        /* Update intensity and temperature proportionally to fuel left */
        if (src->fuel_kg > 0.0f) {
            src->intensity = fminf(1.0f, src->fuel_kg / 10.0f);
            src->temperature = 200.0f + src->intensity * 800.0f;
        } else {
            /* Fire burns out */
            src->is_active   = 0;
            src->intensity   = 0.0f;
            src->temperature = 20.0f;
            src->fuel_kg     = 0.0f;
        }
    }
}

unsigned wildfire_step(const Mountain *mount,
                       FireSystem *fireSys,
                       const WaterSystem *waterSys,
                       float dt)
{
    if (!fireSys || dt <= 0.0f)
        return 0;

    /* 1) Fire consumes fuel & may self-extinguish */
    wildfire_evolve(fireSys, dt);

    /* 2) External extinguishing (e.g., hoses, rain) */
    if (waterSys)
        extinguish_fire_with_water(fireSys, waterSys);

    /* 3) Spread to new areas */
    wildfire_spread(mount, fireSys, dt);

    return fireSys->source_count;
}