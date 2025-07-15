#include <stdio.h>

/* 두 int 값을 서로 교환하는 함수 */
void swap_int(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/* 두 double 값을 서로 교환하는 함수 */
void swap_double(double *a, double *b)
{
    double tmp = *a;
    *a = *b;
    *b = tmp;
}

int main(void)
{
    int i = 10, j = 20;
    double x = 3.14, y = 1.618;

    printf("Before swap_int   : i = %d, j = %d\n", i, j);
    swap_int(&i, &j);
    printf("After  swap_int   : i = %d, j = %d\n\n", i, j);

    printf("Before swap_double: x = %f, y = %f\n", x, y);
    swap_double(&x, &y);
    printf("After  swap_double: x = %f, y = %f\n", x, y);

    return 0;
}