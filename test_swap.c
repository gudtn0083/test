#include <assert.h>
#include <math.h>

/* 함수 원형 선언 (test.c에서 정의됨) */
void swap_int(int *a, int *b);
void swap_double(double *a, double *b);

int main(void)
{
    /* 정수 교환 테스트 */
    int i = 1, j = 2;
    swap_int(&i, &j);
    assert(i == 2 && j == 1);

    /* 실수 교환 테스트 */
    double x = 3.14, y = 2.71;
    swap_double(&x, &y);
    assert(fabs(x - 2.71) < 1e-12 && fabs(y - 3.14) < 1e-12);

    /* 모든 테스트 통과 시 0 반환 */
    return 0;
}