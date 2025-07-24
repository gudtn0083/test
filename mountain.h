#ifndef MOUNTAIN_H
#define MOUNTAIN_H

#include "fire.h"  /* for Vec3 definition */

#ifdef __cplusplus
extern "C" {
#endif

/*----------------------------------------------------------------------------*/
/*  Mountain terrain structure                                                */
/*----------------------------------------------------------------------------*/

typedef struct {
    Vec3  peak_position;      /* World-space coordinates of the summit (m) */
    float height;             /* Elevation above sea level (meters)        */
    float base_radius;        /* Approximate radius of mountain base (m)   */
    float slope_deg;          /* Average slope angle in degrees            */
    float vegetation_density; /* 0.0 (bare rock) … 1.0 (dense forest)      */
} Mountain;

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* MOUNTAIN_H */