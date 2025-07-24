#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "classifier.h"

typedef struct { float dist; const char *label; } Node;

static float distance(const float *a, const float *b, size_t len)
{
    float sum = 0.f;
    for (size_t i = 0; i < len; ++i) {
        float d = a[i] - b[i];
        sum += d * d;
    }
    return sqrtf(sum);
}

static int cmp_node(const void *aa, const void *bb)
{
    float da = ((const Node *)aa)->dist;
    float db = ((const Node *)bb)->dist;
    return (da > db) - (da < db);
}

const char *classify_knn(const Dataset *ds, const float *feature, size_t len, int k)
{
    if (!ds->count)
        return NULL;
    if (k <= 0 || k > (int)ds->count)
        k = (int)ds->count;

    Node *arr = (Node *)malloc(ds->count * sizeof(Node));
    for (size_t i = 0; i < ds->count; ++i) {
        arr[i].dist  = distance(ds->samples[i].feature, feature, len);
        arr[i].label = ds->samples[i].label;
    }
    qsort(arr, ds->count, sizeof(Node), cmp_node);

    /* vote */
    typedef struct { const char *label; int votes; } Vote;
    Vote *votes = NULL;
    size_t vcount = 0;

    for (int i = 0; i < k; ++i) {
        const char *lab = arr[i].label;
        size_t j;
        for (j = 0; j < vcount; ++j)
            if (strcmp(votes[j].label, lab) == 0) { votes[j].votes++; break; }
        if (j == vcount) {
            votes = (Vote *)realloc(votes, (vcount + 1) * sizeof(Vote));
            votes[vcount].label = lab;
            votes[vcount].votes = 1;
            vcount++;
        }
    }

    const char *best = NULL;
    int best_votes = -1;
    for (size_t i = 0; i < vcount; ++i)
        if (votes[i].votes > best_votes) {
            best       = votes[i].label;
            best_votes = votes[i].votes;
        }

    free(votes);
    free(arr);
    return best;
}