#ifndef VOLCANO_H
#define VOLCANO_H

/*
 * Struct: Volcano
 * ----------------
 * Models basic geophysical and historical data about a volcano.
 */
typedef struct {
    char   name[64];            /* Common name of the volcano                */
    double latitude;            /* Geographic latitude in decimal degrees     */
    double longitude;           /* Geographic longitude in decimal degrees    */
    double elevation_m;         /* Elevation above sea level in meters        */
    int    last_eruption_year;  /* Year of the most recent confirmed eruption */
    int    is_active;           /* 1 if considered active, 0 otherwise        */
    char   type[32];            /* Volcano type (e.g., stratovolcano)         */
} Volcano;

#endif /* VOLCANO_H */