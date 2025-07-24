#ifndef FEATURE_H
#define FEATURE_H

#include <stddef.h>

int compute_histogram(const unsigned char *rgb,
                      int                 width,
                      int                 height,
                      int                 channels,
                      float             **out_feat,
                      size_t             *out_len);

#endif // FEATURE_H