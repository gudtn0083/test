#ifndef FLOOD_H
#define FLOOD_H

typedef struct {
    char name[64];
    char country[32];
    char start_date[11];
    char end_date[11];
    long affected_population;
} Flood;

#endif /* FLOOD_H */