#include <math.h>
#include "fire_water.h"

static float distance_vec3(const Vec3 *a, const Vec3 *b)
{
    float dx = a->x - b->x;
    float dy = a->y - b->y;
    float dz = a->z - b->z;
    return sqrtf(dx * dx + dy * dy + dz * dz);
}

unsigned extinguish_fire_with_water(FireSystem *fireSys,
                                    const WaterSystem *waterSys)
{
    if (!fireSys || !waterSys)
        return 0;

    unsigned extinguished = 0;

    for (unsigned i = 0; i < fireSys->source_count; ++i) {
        FireSource *src = &fireSys->sources[i];
        if (!src->is_active)
            continue;

        /* Check all active emitters */
        for (unsigned j = 0; j < waterSys->emitter_count; ++j) {
            const WaterEmitter *em = &waterSys->emitters[j];
            if (!em->is_active)
                continue;

            float dist = distance_vec3(&src->position, &em->position);
            /* Effective radius proportional to sqrt(flow_rate) * 2 */
            float effective_radius = sqrtf(em->flow_rate_lps) * 2.0f;

            if (dist <= effective_radius) {
                /* Extinguish the fire */
                src->is_active   = 0;
                src->intensity   = 0.0f;
                src->temperature = 20.0f;  /* ambient */
                src->fuel_kg     = 0.0f;

                ++extinguished;
                break; /* No need to check more emitters for this fire */
            }
        }
    }

    return extinguished;
}