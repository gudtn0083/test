#ifndef CLASSIFIER_H
#define CLASSIFIER_H

#include "dataset.h"

const char *classify_knn(const Dataset *ds,
                         const float   *feature,
                         size_t         feat_len,
                         int            k);

#endif // CLASSIFIER_H