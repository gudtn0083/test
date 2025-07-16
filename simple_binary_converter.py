import cv2
import matplotlib
matplotlib.use('Agg')  # GUI가 없는 환경에서 사용
import matplotlib.pyplot as plt

def convert_image_to_binary(image_path):
    """
    이미지를 이진 이미지로 변환하는 간단한 함수
    """
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Otsu 방법으로 이진화 (자동으로 최적 임계값 결정)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return gray, binary

# 이미지 변환 실행
image_path = "Test1.PNG"  # 여기에 원하는 이미지 파일명 입력

try:
    gray, binary = convert_image_to_binary(image_path)
    
    # 결과 표시
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title('원본 이미지')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(binary, cmap='gray')
    plt.title('이진 이미지')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # 이진 이미지 저장
    cv2.imwrite('binary_output.png', binary)
    print("이진 이미지가 'binary_output.png'로 저장되었습니다.")
    
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
    print("이미지 파일 경로를 확인해주세요.")