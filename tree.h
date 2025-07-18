#ifndef TREE_H
#define TREE_H

#ifdef __cplusplus
extern "C" {
#endif

/* Binary tree node structure */
typedef struct TreeNode {
    int value;                  /* value stored in the node */
    struct TreeNode *left;      /* pointer to the left child */
    struct TreeNode *right;     /* pointer to the right child */
} TreeNode;

/* Binary tree wrapper structure */
typedef struct BinaryTree {
    TreeNode *root;             /* pointer to the root node */
} BinaryTree;

/* Node-level helpers */
TreeNode *create_node(int value);
void      destroy_node(TreeNode *node);

/* Tree-level helpers */
BinaryTree *create_tree(void);
void        destroy_tree(BinaryTree *tree);

int  insert(BinaryTree *tree, int value);
int  search(const BinaryTree *tree, int value);
void preorder(const BinaryTree *tree, void (*visit)(int));
void inorder(const BinaryTree *tree, void (*visit)(int));
void postorder(const BinaryTree *tree, void (*visit)(int));

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* TREE_H */