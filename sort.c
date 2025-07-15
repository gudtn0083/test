#include "sort.h"

/* 정수 배열을 오름차순으로 정렬 (버블 정렬) */
void sort_int_asc(int arr[], size_t n)
{
    for (size_t i = 0; i < n - 1; ++i) {
        for (size_t j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}

/* 실수 배열을 오름차순으로 정렬 (버블 정렬) */
void sort_double_asc(double arr[], size_t n)
{
    for (size_t i = 0; i < n - 1; ++i) {
        for (size_t j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                double tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}