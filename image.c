#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "image.h"

unsigned char *load_image_rgb(const char *filename, int *w, int *h)
{
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        perror("fopen");
        return NULL;
    }

    char magic[3] = {0};
    if (fscanf(fp, "%2s", magic) != 1 || strcmp(magic, "P6") != 0) {
        fprintf(stderr, "%s: not a binary PPM (P6).\n", filename);
        fclose(fp);
        return NULL;
    }

    int width, height, maxval;
    if (fscanf(fp, "%d %d %d", &width, &height, &maxval) != 3) {
        fprintf(stderr, "%s: malformed PPM header.\n", filename);
        fclose(fp);
        return NULL;
    }

    fgetc(fp); /* consume single whitespace after header */

    size_t size = (size_t)width * height * 3;
    unsigned char *data = (unsigned char *)malloc(size);
    if (!data) {
        fclose(fp);
        return NULL;
    }

    if (fread(data, 1, size, fp) != size) {
        fprintf(stderr, "%s: unexpected EOF.\n", filename);
        free(data);
        fclose(fp);
        return NULL;
    }
    fclose(fp);

    *w = width;
    *h = height;
    return data;
}

void free_image(unsigned char *data) { free(data); }