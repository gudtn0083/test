#ifndef WATER_H
#define WATER_H

#ifdef __cplusplus
extern "C" {
#endif

/*-------------------------------------------------------------------------*/
/*  Water-related data structures                                          */
/*-------------------------------------------------------------------------*/
/*  NOTE: This header pulls in Vec3 and ColorRGB definitions from fire.h   */
/*        to avoid code duplication. If you do not use fire.h in your      */
/*        project, copy those typedefs here or refactor into a common file.*/
/*-------------------------------------------------------------------------*/

#include "fire.h"   /* for Vec3 and ColorRGB */

/* Continuous water emitter (e.g., hose, faucet) -------------------------- */
typedef struct {
    Vec3  position;      /* World-space origin (meters)                   */
    float flow_rate_lps; /* Flow rate (litres per second)                 */
    float temperature;   /* Water temperature (°C)                        */
    int   is_active;     /* Non-zero while emitter is turned on           */
} WaterEmitter;

/* Individual droplet/particle used for spray or splash effects ----------- */
typedef struct {
    Vec3   position;     /* Current position (meters)                     */
    Vec3   velocity;     /* Current velocity (m/s)                        */
    float  lifetime;     /* Remaining lifetime (seconds)                  */
    float  size;         /* Diameter (meters)                             */
    float  opacity;      /* 0.0 (transparent) … 1.0 (opaque)              */
} WaterParticle;

/* Representation of a planar water surface (pool, lake, ocean patch) ---- */
typedef struct {
    Vec3  center;        /* Center point of the surface patch (meters)    */
    float width;         /* Patch width  (meters)                         */
    float length;        /* Patch length (meters)                         */
    float depth;         /* Average depth (meters)                        */
    float wave_height;   /* Wave amplitude (meters)                       */
    float wave_speed;    /* Wave phase velocity (m/s)                     */
} WaterSurface;

/* Top-level water simulation container ----------------------------------- */
typedef struct {
    WaterEmitter  *emitters;        /* Dynamic array of emitters           */
    unsigned       emitter_count;

    WaterParticle *particles;       /* Dynamic array of droplets           */
    unsigned       particle_count;

    WaterSurface  *surfaces;        /* Dynamic array of surface patches    */
    unsigned       surface_count;

    float global_current_speed;     /* Ambient water current speed (m/s)   */
    Vec3  global_current_direction; /* Normalised current direction        */
} WaterSystem;

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* WATER_H */