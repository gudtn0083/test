import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # GUI가 없는 환경에서 사용
import matplotlib.pyplot as plt
from PIL import Image

def convert_to_binary(image_path, method='otsu', threshold_value=127):
    """
    이미지를 이진 이미지로 변환하는 함수
    
    Parameters:
    - image_path: 입력 이미지 파일 경로
    - method: 이진화 방법 ('otsu', 'adaptive', 'simple')
    - threshold_value: 단순 임계값 방법에서 사용할 임계값 (0-255)
    
    Returns:
    - binary_image: 이진화된 이미지
    """
    
    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if method == 'otsu':
        # Otsu의 이진화 (자동으로 최적 임계값 찾기)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"Otsu 방법으로 자동 설정된 임계값: {_}")
        
    elif method == 'adaptive':
        # 적응형 임계값 이진화
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
    elif method == 'simple':
        # 단순 임계값 이진화
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        
    else:
        raise ValueError("지원하지 않는 방법입니다. 'otsu', 'adaptive', 'simple' 중 선택하세요.")
    
    return binary, gray

def display_results(original_gray, binary_image, method):
    """결과 이미지들을 화면에 표시"""
    plt.figure(figsize=(12, 4))
    
    # 원본 그레이스케일 이미지
    plt.subplot(1, 2, 1)
    plt.imshow(original_gray, cmap='gray')
    plt.title('원본 (그레이스케일)')
    plt.axis('off')
    
    # 이진화된 이미지
    plt.subplot(1, 2, 2)
    plt.imshow(binary_image, cmap='gray')
    plt.title(f'이진 이미지 ({method})')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def save_binary_image(binary_image, output_path):
    """이진화된 이미지를 파일로 저장"""
    cv2.imwrite(output_path, binary_image)
    print(f"이진 이미지가 저장되었습니다: {output_path}")

def main():
    # 이미지 파일 경로 설정
    input_image = "Test1.PNG"  # 입력 이미지 파일명
    
    print("=== 이미지 이진화 프로그램 ===")
    print(f"입력 이미지: {input_image}")
    
    try:
        # 다양한 방법으로 이진화 수행
        methods = ['otsu', 'adaptive', 'simple']
        
        for method in methods:
            print(f"\n--- {method.upper()} 방법으로 이진화 ---")
            
            if method == 'simple':
                binary, gray = convert_to_binary(input_image, method, threshold_value=127)
            else:
                binary, gray = convert_to_binary(input_image, method)
            
            # 결과 표시
            display_results(gray, binary, method)
            
            # 이진화된 이미지 저장
            output_filename = f"binary_{method}_{input_image}"
            save_binary_image(binary, output_filename)
            
    except Exception as e:
        print(f"오류 발생: {e}")

# 개별 함수들을 테스트하기 위한 예제
def quick_binary_convert(image_path, output_path=None):
    """빠른 이진화 변환 (Otsu 방법 사용)"""
    binary, gray = convert_to_binary(image_path, 'otsu')
    
    if output_path:
        save_binary_image(binary, output_path)
    
    # 간단한 결과 표시
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title('원본')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(binary, cmap='gray')
    plt.title('이진 이미지')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return binary

if __name__ == "__main__":
    # 메인 프로그램 실행
    main()
    
    # 또는 빠른 변환을 원한다면:
    # binary_result = quick_binary_convert("Test1.PNG", "binary_output.png")