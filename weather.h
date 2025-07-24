#ifndef WEATHER_H
#define WEATHER_H

#include "fire.h" /* Vec3 for direction */

#ifdef __cplusplus
extern "C" {
#endif

/*----------------------------------------------------------------------------*/
/*  Weather description structure                                             */
/*----------------------------------------------------------------------------*/

/*! Atmospheric and environmental conditions that influence wildfire. */
typedef struct {
    float  temperature;          /* Ambient temperature (°C)             */
    float  humidity;             /* Relative humidity (0.0-1.0)          */
    float  precipitation_mmph;   /* Rainfall intensity (mm per hour)     */
    float  wind_speed;           /* Wind speed (m/s)                     */
    Vec3   wind_direction;       /* Normalised wind direction vector     */
} Weather;

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* WEATHER_H */