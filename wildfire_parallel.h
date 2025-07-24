#ifndef WILDFIRE_PARALLEL_H
#define WILDFIRE_PARALLEL_H

#include "mountain.h"
#include "fire.h"
#include "water.h"
#include "weather.h"
#include "fire_water.h"

#ifdef __cplusplus
extern "C" {
#endif

/*===========================================================================*/
/*  Parallel wildfire simulation                                             */
/*===========================================================================*/

/* Advance the wildfire simulation by dt seconds using multiple threads.
 * `threads` selects how many worker threads to request (<=0 → default). */
unsigned wildfire_step_parallel(const Mountain *mount,
                                FireSystem      *fireSys,
                                const WaterSystem *waterSys,
                                const Weather   *weather,
                                float            dt,
                                int              threads);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* WILDFIRE_PARALLEL_H */