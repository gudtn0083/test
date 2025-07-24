#ifndef DATASET_H
#define DATASET_H

#include <stddef.h>

typedef struct {
    char  *label;
    float *feature;
} Sample;

typedef struct {
    Sample *samples;
    size_t  count;
    size_t  feature_len;
} Dataset;

int  load_dataset(const char *root, Dataset *ds);
void free_dataset(Dataset *ds);

#endif // DATASET_H