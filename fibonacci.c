#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    long n = 10; /* default length */
    if (argc >= 2) {
        n = strtol(argv[1], NULL, 10);
        if (n <= 0) {
            fprintf(stderr, "양의 정수를 입력하세요.\n");
            return 1;
        }
    }

    printf("Fibonacci sequence (first %ld terms):\n", n);

    unsigned long long a = 0, b = 1;
    for (long i = 0; i < n; ++i) {
        printf("%llu", (unsigned long long)(i == 0 ? a : b));
        if (i < n - 1) printf(", ");
        /* update sequence */
        unsigned long long next = a + b;
        a = b;
        b = next;
    }
    printf("\n");
    return 0;
}