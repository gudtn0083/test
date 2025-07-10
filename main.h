#ifndef MAIN_H
#define MAIN_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 함수 선언
void printHello();
int add(int a, int b);
void printArray(int arr[], int size);

// 상수 정의
#define MAX_SIZE 100
#define PI 3.14159

// 구조체 정의
typedef struct {
    int x;
    int y;
} Point;

// 함수 구현
void printHello() {
    printf("Hello, World!\n");
}

int add(int a, int b) {
    return a + b;
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

#endif // MAIN_H