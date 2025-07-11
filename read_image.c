#include <stdio.h>
#include <opencv2/core/core_c.h>
#include <opencv2/highgui/highgui_c.h>

int main(int argc, char *argv[])
{
    if (argc < 2) {
        printf("사용법: %s <image_path>\n", argv[0]);
        return 1;
    }

    const char *filePath = argv[1];

    /* 이미지 읽기 (컬러 BGR 모드) */
    IplImage *img = cvLoadImage(filePath, CV_LOAD_IMAGE_COLOR);
    if (img == NULL) {
        fprintf(stderr, "이미지를 읽을 수 없습니다: %s\n", filePath);
        return 1;
    }

    printf("이미지 정보를 표시합니다.\n");
    printf("  파일명 : %s\n", filePath);
    printf("  가로(px): %d\n", img->width);
    printf("  세로(px): %d\n", img->height);
    printf("  채널 수 : %d (BGR)\n", img->nChannels);

    /* 화면에 표시 (선택사항) */
    cvNamedWindow("Image", CV_WINDOW_AUTOSIZE);
    cvShowImage("Image", img);
    printf("윈도우를 닫으면 프로그램이 종료됩니다...\n");
    cvWaitKey(0);

    /* 메모리 해제 */
    cvReleaseImage(&img);
    cvDestroyWindow("Image");
    return 0;
}