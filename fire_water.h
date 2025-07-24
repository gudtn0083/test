#ifndef FIRE_WATER_H
#define FIRE_WATER_H

#include "fire.h"
#include "water.h"

#ifdef __cplusplus
extern "C" {
#endif

/*--------------------------------------------------------------------------*/
/*  Fire & Water interaction utilities                                      */
/*--------------------------------------------------------------------------*/

/*!
 * Extinguish active fires that are within range of active water emitters.
 *
 * Simple heuristic: if the distance between a FireSource and a WaterEmitter
 * is less than an effective radius derived from \f$\sqrt{flow\_rate}\times2\f$,
 * the fire is considered extinguished. The function sets the fire's
 * `is_active` flag to 0, zeroes its intensity and fuel, and cools the
 * temperature to a nominal 20 °C.
 *
 * \param fireSys   Fire system to modify.
 * \param waterSys  Water system supplying the extinguishing emitters.
 * \return Number of fire sources that were extinguished.
 */
unsigned extinguish_fire_with_water(struct FireSystem *fireSys,
                                    const struct WaterSystem *waterSys);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* FIRE_WATER_H */