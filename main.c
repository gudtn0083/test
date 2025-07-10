#include "main.h"

int main() {
    printf("=== C 프로그램 시작 ===\n");
    
    // 헤더 파일의 함수들 사용
    printHello();
    
    int result = add(5, 3);
    printf("5 + 3 = %d\n", result);
    
    // 배열 예제
    int numbers[] = {1, 2, 3, 4, 5};
    printf("배열 출력: ");
    printArray(numbers, 5);
    
    // 구조체 사용
    Point p = {10, 20};
    printf("점의 좌표: (%d, %d)\n", p.x, p.y);
    
    // 상수 사용
    printf("MAX_SIZE: %d\n", MAX_SIZE);
    printf("PI: %.5f\n", PI);
    
    printf("=== 프로그램 종료 ===\n");
    return 0;
}