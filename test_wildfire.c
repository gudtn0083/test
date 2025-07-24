#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "wildfire_parallel.h"

static void init_simulation(Mountain *m, FireSystem *fires, WaterSystem *water, Weather *w)
{
    /* Mountain */
    m->peak_position = (Vec3){0,0,1000};
    m->height = 1200.0f;
    m->base_radius = 800.0f;
    m->slope_deg = 25.0f;
    m->vegetation_density = 0.8f;

    /* FireSystem */
    fires->sources = (FireSource*)calloc(1, sizeof(FireSource));
    fires->source_count = 1;
    fires->particles = NULL; fires->particle_count = 0;
    fires->wind_speed = 0.0f;
    fires->wind_direction = (Vec3){1,0,0};

    FireSource *seed = &fires->sources[0];
    *seed = (FireSource){
        .position = {0,0,0},
        .radius = 2.0f,
        .temperature = 600.0f,
        .intensity = 1.0f,
        .fuel_kg = 10.0f,
        .is_active = 1
    };

    /* WaterSystem (initially off) */
    water->emitters = (WaterEmitter*)calloc(1, sizeof(WaterEmitter));
    water->emitter_count = 1;
    water->particles = NULL; water->particle_count = 0;
    water->surfaces = NULL;  water->surface_count = 0;
    water->global_current_speed = 0.0f;
    water->global_current_direction = (Vec3){0,0,0};

    WaterEmitter *hose = &water->emitters[0];
    *hose = (WaterEmitter){
        .position = {5,0,0},
        .flow_rate_lps = 0.0f,
        .temperature = 15.0f,
        .is_active = 0
    };

    /* Weather */
    *w = (Weather){
        .temperature = 30.0f,
        .humidity = 0.3f,
        .precipitation_mmph = 0.0f,
        .wind_speed = 5.0f,
        .wind_direction = {1,0,0}
    };
}

int main(void)
{
    srand((unsigned)time(NULL));

    Mountain mountain;
    FireSystem fires = {0};
    WaterSystem water = {0};
    Weather weather;

    init_simulation(&mountain, &fires, &water, &weather);

    const float dt = 1.0f;   /* seconds */
    const int   steps = 60;  /* simulate 1 minute */

    for (int t = 0; t < steps; ++t) {
        /* Turn on hose after 30 s */
        if (t == 30) {
            water.emitters[0].flow_rate_lps = 10.0f;
            water.emitters[0].is_active = 1;
            printf("[%.2f] Hose activated!\n", t*dt);
        }

        unsigned count = wildfire_step_parallel(&mountain, &fires, &water, &weather, dt, 4);
        printf("[%.2f] Active fires: %u\n", t*dt, count);
    }

    /* Cleanup */
    free(fires.sources);
    free(water.emitters);
    return 0;
}