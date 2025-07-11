#include <stdio.h>
#include <opencv2/core/core_c.h>
#include <opencv2/highgui/highgui_c.h>

int main(int argc, char *argv[])
{
    if (argc < 2) {
        printf("사용법: %s <image_path> [threshold (0-255)]\n", argv[0]);
        return 1;
    }

    const char *filePath = argv[1];
    int thresholdValue = 128; /* 기본 임계값 */
    if (argc >= 3) {
        /* 사용자가 임계값을 지정한 경우 */
        thresholdValue = atoi(argv[2]);
        if (thresholdValue < 0 || thresholdValue > 255) {
            fprintf(stderr, "임계값은 0에서 255 사이여야 합니다.\n");
            return 1;
        }
    }

    /* 그레이스케일로 이미지 읽기 */
    IplImage *gray = cvLoadImage(filePath, CV_LOAD_IMAGE_GRAYSCALE);
    if (gray == NULL) {
        fprintf(stderr, "이미지를 읽을 수 없습니다: %s\n", filePath);
        return 1;
    }

    /* 이진화 결과를 저장할 이미지 생성 */
    IplImage *binary = cvCreateImage(cvGetSize(gray), IPL_DEPTH_8U, 1);

    /* 임계값 기반 이진화 */
    cvThreshold(gray, binary, thresholdValue, 255, CV_THRESH_BINARY);

    /* 결과 저장 */
    const char *outputPath = "binary_output.png";
    if (!cvSaveImage(outputPath, binary, 0)) {
        fprintf(stderr, "이진 이미지 저장 실패: %s\n", outputPath);
    } else {
        printf("이진 이미지가 저장되었습니다: %s\n", outputPath);
    }

    /* 결과 정보 출력 */
    printf("원본 파일 : %s\n", filePath);
    printf("가로(px) : %d\n", gray->width);
    printf("세로(px) : %d\n", gray->height);
    printf("채널     : 1 (Grayscale/Binary)\n");
    printf("사용 임계값: %d\n", thresholdValue);

    /* 화면에 표시 (선택 사항) */
    cvNamedWindow("Binary Image", CV_WINDOW_AUTOSIZE);
    cvShowImage("Binary Image", binary);
    printf("윈도우를 닫으면 프로그램이 종료됩니다...\n");
    cvWaitKey(0);

    /* 메모리 해제 */
    cvReleaseImage(&gray);
    cvReleaseImage(&binary);
    cvDestroyWindow("Binary Image");

    return 0;
}