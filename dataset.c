#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include "dataset.h"
#include "image.h"
#include "feature.h"

static int has_suffix(const char *name, const char *suf)
{
    size_t n = strlen(name), m = strlen(suf);
    return n >= m && strcmp(name + n - m, suf) == 0;
}

static void add_sample(Dataset *ds, const char *label, float *feat)
{
    ds->samples = (Sample *)realloc(ds->samples, (ds->count + 1) * sizeof(Sample));
    ds->samples[ds->count].label   = strdup(label);
    ds->samples[ds->count].feature = feat;
    ds->count++;
}

int load_dataset(const char *root, Dataset *ds)
{
    memset(ds, 0, sizeof(*ds));

    struct dirent **labels;
    int nlabels = scandir(root, &labels, NULL, alphasort);
    if (nlabels < 0) {
        perror("scandir");
        return -1;
    }

    for (int i = 0; i < nlabels; ++i) {
        const char *lname = labels[i]->d_name;
        if (lname[0] == '.') { free(labels[i]); continue; }

        char lpath[4096];
        snprintf(lpath, sizeof lpath, "%s/%s", root, lname);

        struct stat st;
        if (stat(lpath, &st) != 0 || !S_ISDIR(st.st_mode)) { free(labels[i]); continue; }

        struct dirent **imgs;
        int nimg = scandir(lpath, &imgs, NULL, alphasort);
        if (nimg < 0) { free(labels[i]); continue; }

        for (int j = 0; j < nimg; ++j) {
            const char *fname = imgs[j]->d_name;
            if (fname[0] == '.' || !has_suffix(fname, ".ppm")) { free(imgs[j]); continue; }

            char fpath[4096];
            snprintf(fpath, sizeof fpath, "%s/%s", lpath, fname);

            int w, h;
            unsigned char *img = load_image_rgb(fpath, &w, &h);
            if (!img) { free(imgs[j]); continue; }

            float *feat; size_t flen;
            if (compute_histogram(img, w, h, 3, &feat, &flen) == 0) {
                add_sample(ds, lname, feat);
                ds->feature_len = flen;
            }
            free_image(img);
            free(imgs[j]);
        }
        free(imgs);
        free(labels[i]);
    }
    free(labels);

    return ds->count ? 0 : -1;
}

void free_dataset(Dataset *ds)
{
    for (size_t i = 0; i < ds->count; ++i) {
        free(ds->samples[i].label);
        free(ds->samples[i].feature);
    }
    free(ds->samples);
    memset(ds, 0, sizeof(*ds));
}