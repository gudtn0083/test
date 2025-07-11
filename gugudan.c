#include <stdio.h>

int main(void) {
    for (int i = 2; i <= 9; ++i) {
        printf("=== %d단 ===\n", i);
        for (int j = 1; j <= 9; ++j) {
            printf("%d x %d = %2d\n", i, j, i * j);
        }
        printf("\n");
    }
    return 0;
}