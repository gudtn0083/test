#ifndef WILDFIRE_H
#define WILDFIRE_H

#include "fire.h"
#include "water.h"
#include "mountain.h"
#include "fire_water.h" /* for extinguish integration */

#ifdef __cplusplus
extern "C" {
#endif

/*===========================================================================*
 *  Wildfire simulation utilities                                            *
 *===========================================================================*/

/* Advance wildfire spread based on mountain vegetation, slope and wind.
 * dt is the time step in seconds.                                           */
void wildfire_spread(const Mountain *mount, FireSystem *fireSys, float dt);

/* Update burning state of each fire source (fuel consumption, intensity
 * decay, auto-extinguish when fuel is gone). dt is the time step in seconds.*/
void wildfire_evolve(FireSystem *fireSys, float dt);

/* Convenience helper that evolves, extinguishes with water, and then spreads
 * the wildfire in a single call.                                           */
unsigned wildfire_step(const Mountain *mount,
                       FireSystem *fireSys,
                       const WaterSystem *waterSys,
                       float dt);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* WILDFIRE_H */