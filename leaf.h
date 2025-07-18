#ifndef LEAF_H
#define LEAF_H

#ifdef __cplusplus
extern "C" {
#endif

/* Enumeration for leaf color */
typedef enum {
    LEAF_GREEN,
    LEAF_YELLOW,
    LEAF_BROWN,
    LEAF_RED
} LeafColor;

/* Leaf structure */
typedef struct Leaf {
    LeafColor color; /* color of the leaf */
    float length;    /* length in centimeters */
    float width;     /* width  in centimeters */
} Leaf;

/* Leaf helpers */
Leaf *create_leaf(LeafColor color, float length, float width);
void  destroy_leaf(Leaf *leaf);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* LEAF_H */