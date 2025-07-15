#include <stdio.h>
#include <assert.h>
#include "sort.h"

int main(void)
{
    int arr_i[] = {5, 3, 8, 1, 4};
    const int n_i = sizeof(arr_i) / sizeof(arr_i[0]);
    sort_int_asc(arr_i, n_i);

    /* 정렬 결과 확인 */
    for (int k = 0; k < n_i - 1; ++k) {
        assert(arr_i[k] <= arr_i[k + 1]);
    }

    double arr_d[] = {3.14, -1.0, 2.71, 0.0};
    const int n_d = sizeof(arr_d) / sizeof(arr_d[0]);
    sort_double_asc(arr_d, n_d);

    /* 실수 배열 정렬 확인 */
    for (int k = 0; k < n_d - 1; ++k) {
        assert(arr_d[k] <= arr_d[k + 1]);
    }

    /* 통과 시 출력 */
    printf("All sort tests passed!\n");
    return 0;
}