#ifndef FIRE_H
#define FIRE_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Data structures for representing and simulating fire-related entities.
 * These are intentionally kept generic so they can be reused in games,
 * simulations, or embedded applications that need to track fire dynamics.
 */

/* 3-D vector helper ------------------------------------------------------- */
typedef struct {
    float x;    /* X coordinate */
    float y;    /* Y coordinate */
    float z;    /* Z coordinate */
} Vec3;

/* RGB color expressed as floating-point values (0.0-1.0) ------------------ */
typedef struct {
    float r;    /* Red   component */
    float g;    /* Green component */
    float b;    /* Blue  component */
} ColorRGB;

/* Main fire descriptor ---------------------------------------------------- */
typedef struct {
    Vec3      position;      /* World-space origin of the fire (meters)   */
    float     radius;        /* Affected radius (meters)                  */
    float     temperature;   /* Temperature at the core (°C)             */
    float     intensity;     /* Normalised 0.0-1.0 intensity factor      */
    float     fuel_kg;       /* Remaining fuel mass (kilograms)          */
    int       is_active;     /* Non-zero while the fire is burning       */
} FireSource;

/* Individual particle used for visual smoke/flame simulation ------------- */
typedef struct {
    Vec3      position;      /* Current position (meters)                */
    Vec3      velocity;      /* Current velocity (m/s)                   */
    float     lifetime;      /* Remaining lifetime (seconds)             */
    float     size;          /* Current particle size (meters)           */
    ColorRGB  color;         /* Current particle colour                  */
} FireParticle;

/* A container representing a full fire simulation ------------------------ */
typedef struct {
    FireSource *sources;     /* Dynamic array of active fire sources     */
    unsigned    source_count;

    FireParticle *particles; /* Dynamic array of particles               */
    unsigned     particle_count;

    float wind_speed;        /* Environmental wind speed (m/s)           */
    Vec3  wind_direction;    /* Normalised wind direction vector         */
} FireSystem;

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* FIRE_H */