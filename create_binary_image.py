#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def create_simple_binary_image():
    """간단한 이진 이미지 생성"""
    # 200x200 크기의 빈 이미지 생성
    img = np.zeros((200, 200), dtype=np.uint8)
    
    # 원과 사각형 그리기 (흰색, 값 255)
    cv2.circle(img, (50, 50), 30, 255, -1)  # 원
    cv2.rectangle(img, (100, 100), (180, 180), 255, -1)  # 사각형
    
    return img

def create_text_binary_image():
    """텍스트가 포함된 이진 이미지 생성"""
    img = np.zeros((150, 400), dtype=np.uint8)
    
    # 텍스트 추가
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Binary Image', (50, 75), font, 1, 255, 2)
    
    return img

def create_pattern_binary_image():
    """패턴이 있는 이진 이미지 생성"""
    img = np.zeros((200, 200), dtype=np.uint8)
    
    # 체스보드 패턴 생성
    for i in range(0, 200, 20):
        for j in range(0, 200, 20):
            if (i//20 + j//20) % 2 == 0:
                img[i:i+20, j:j+20] = 255
    
    return img

def convert_to_binary(image_path):
    """기존 이미지를 이진 이미지로 변환"""
    if os.path.exists(image_path):
        # 이미지 읽기
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # 이진화 (임계값 127)
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        
        return binary
    else:
        print(f"이미지 파일 {image_path}을 찾을 수 없습니다.")
        return None

def main():
    print("이진 이미지 생성 중...")
    
    # 1. 간단한 도형이 있는 이진 이미지
    binary1 = create_simple_binary_image()
    cv2.imwrite('binary_shapes.png', binary1)
    print("✓ 도형이 있는 이진 이미지 저장: binary_shapes.png")
    
    # 2. 텍스트가 있는 이진 이미지
    binary2 = create_text_binary_image()
    cv2.imwrite('binary_text.png', binary2)
    print("✓ 텍스트가 있는 이진 이미지 저장: binary_text.png")
    
    # 3. 패턴이 있는 이진 이미지
    binary3 = create_pattern_binary_image()
    cv2.imwrite('binary_pattern.png', binary3)
    print("✓ 패턴이 있는 이진 이미지 저장: binary_pattern.png")
    
    # 시각화를 위한 matplotlib 사용
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(binary1, cmap='gray')
    axes[0].set_title('Shapes')
    axes[0].axis('off')
    
    axes[1].imshow(binary2, cmap='gray')
    axes[1].set_title('Text')
    axes[1].axis('off')
    
    axes[2].imshow(binary3, cmap='gray')
    axes[2].set_title('Pattern')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('binary_images_preview.png', dpi=150, bbox_inches='tight')
    print("✓ 미리보기 이미지 저장: binary_images_preview.png")
    
    print("\n생성된 이진 이미지들:")
    print("- binary_shapes.png: 원과 사각형이 있는 이진 이미지")
    print("- binary_text.png: 텍스트가 있는 이진 이미지") 
    print("- binary_pattern.png: 체스보드 패턴 이진 이미지")
    print("- binary_images_preview.png: 모든 이미지의 미리보기")

if __name__ == "__main__":
    main()