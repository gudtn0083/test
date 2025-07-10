#include "utils.h"

int main() {
    printf("=== 유틸리티 함수 예제 ===\n\n");
    
    // 문자열 유틸리티 테스트
    printf("1. 문자열 유틸리티:\n");
    char str[] = "Hello World";
    printf("원본 문자열: %s\n", str);
    
    reverseString(str);
    printf("뒤집힌 문자열: %s\n", str);
    
    reverseString(str); // 다시 뒤집어서 원래대로
    toUpperCase(str);
    printf("대문자 변환: %s\n", str);
    
    toLowerCase(str);
    printf("소문자 변환: %s\n", str);
    printf("문자열 길이: %d\n\n", stringLength(str));
    
    // 수학 유틸리티 테스트
    printf("2. 수학 유틸리티:\n");
    int num = 5;
    printf("%d! = %d\n", num, factorial(num));
    printf("%d는 소수인가? %s\n", num, isPrime(num) ? "예" : "아니오");
    printf("GCD(12, 18) = %d\n", gcd(12, 18));
    printf("LCM(12, 18) = %d\n\n", lcm(12, 18));
    
    // 배열 유틸리티 테스트
    printf("3. 배열 유틸리티:\n");
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int size = sizeof(arr) / sizeof(arr[0]);
    
    printf("원본 배열: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    int arr_copy[7];
    memcpy(arr_copy, arr, sizeof(arr));
    
    bubbleSort(arr_copy, size);
    printf("버블 정렬 후: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr_copy[i]);
    }
    printf("\n");
    
    printf("최대값: %d\n", findMax(arr, size));
    printf("최소값: %d\n", findMin(arr, size));
    
    int target = 25;
    int index = binarySearch(arr_copy, size, target);
    printf("%d의 위치: %s\n\n", target, index != -1 ? "찾음" : "못찾음");
    
    // 파일 유틸리티 테스트
    printf("4. 파일 유틸리티:\n");
    writeToFile("test_output.txt", "이것은 테스트 파일입니다.\n");
    printf("파일 쓰기 완료\n");
    
    char* content = readFromFile("test_output.txt");
    if (content != NULL) {
        printf("파일 읽기: %s", content);
        free(content);
    }
    
    appendToFile("test_output.txt", "추가된 내용입니다.\n");
    printf("파일 추가 완료\n\n");
    
    // 시간 유틸리티 테스트
    printf("5. 시간 유틸리티:\n");
    printCurrentTime();
    printf("1초 대기 중...\n");
    delay(1000);
    printCurrentTime();
    
    printf("\n=== 예제 완료 ===\n");
    return 0;
}