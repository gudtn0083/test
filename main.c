#include <stdio.h>
#include <stdlib.h>
#include "dataset.h"
#include "image.h"
#include "feature.h"
#include "classifier.h"

int main(int argc, char *argv[])
{
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <dataset_dir> <image.ppm>\n", argv[0]);
        return 1;
    }

    const char *dataset_dir = argv[1];
    const char *image_file  = argv[2];

    Dataset dataset;
    if (load_dataset(dataset_dir, &dataset) != 0) {
        fprintf(stderr, "Failed to load dataset from %s\n", dataset_dir);
        return 1;
    }

    int w, h;
    unsigned char *img = load_image_rgb(image_file, &w, &h);
    if (!img) {
        fprintf(stderr, "Could not load %s\n", image_file);
        free_dataset(&dataset);
        return 1;
    }

    float  *feature;
    size_t  feat_len;
    if (compute_histogram(img, w, h, 3, &feature, &feat_len) != 0) {
        fprintf(stderr, "Could not compute feature vector.\n");
        free_image(img);
        free_dataset(&dataset);
        return 1;
    }

    const char *label = classify_knn(&dataset, feature, feat_len, 3);
    if (label)
        printf("Predicted label: %s\n", label);
    else
        printf("Could not classify the image.\n");

    free(feature);
    free_image(img);
    free_dataset(&dataset);
    return 0;
}