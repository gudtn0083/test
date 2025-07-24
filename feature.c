#include <stdlib.h>
#include <string.h>
#include "feature.h"

int compute_histogram(const unsigned char *rgb,
                      int                 width,
                      int                 height,
                      int                 channels,
                      float             **out_feat,
                      size_t             *out_len)
{
    if (channels < 3)
        return -1;

    const int BINS = 16;               /* per channel */
    const size_t LEN = BINS * 3;       /* R + G + B  */

    float *hist = (float *)calloc(LEN, sizeof(float));
    if (!hist)
        return -1;

    size_t pixels = (size_t)width * height;
    for (size_t i = 0; i < pixels; ++i) {
        unsigned char r = rgb[i * channels + 0];
        unsigned char g = rgb[i * channels + 1];
        unsigned char b = rgb[i * channels + 2];

        hist[(r * BINS) >> 8]            += 1.f;
        hist[BINS + ((g * BINS) >> 8)]   += 1.f;
        hist[2 * BINS + ((b * BINS) >> 8)] += 1.f;
    }

    for (size_t i = 0; i < LEN; ++i)
        hist[i] /= (float)pixels;       /* normalise */

    *out_feat = hist;
    *out_len  = LEN;
    return 0;
}