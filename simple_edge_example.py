#!/usr/bin/env python3
"""
간단한 윤곽선 추출 예제 스크립트
"""

from edge_detector import EdgeDetector
import matplotlib.pyplot as plt

def simple_example():
    """간단한 윤곽선 추출 예제"""
    
    # 이미지 파일 경로 (기본값: Test1.PNG)
    image_path = "Test1.PNG"
    
    try:
        print("이미지 윤곽선 추출을 시작합니다...")
        
        # EdgeDetector 객체 생성
        detector = EdgeDetector(image_path)
        
        # 다양한 방법으로 윤곽선 추출
        print("1. Canny Edge Detection 적용 중...")
        canny_edges = detector.canny_edge_detection()
        
        print("2. Sobel Edge Detection 적용 중...")
        sobel_edges = detector.sobel_edge_detection()
        
        print("3. 결과 저장 중...")
        # 모든 결과를 파일로 저장
        detector.save_results('output')
        
        print("4. 결과 화면에 표시 중...")
        # 결과를 화면에 표시
        plt.figure(figsize=(15, 5))
        
        # 원본 이미지
        plt.subplot(1, 3, 1)
        original_rgb = detector.process_all_methods()['original']
        plt.imshow(original_rgb)
        plt.title('원본 이미지')
        plt.axis('off')
        
        # Canny Edge
        plt.subplot(1, 3, 2)
        plt.imshow(canny_edges, cmap='gray')
        plt.title('Canny Edge Detection')
        plt.axis('off')
        
        # Sobel Edge
        plt.subplot(1, 3, 3)
        plt.imshow(sobel_edges, cmap='gray')
        plt.title('Sobel Edge Detection')
        plt.axis('off')
        
        plt.tight_layout()
        plt.savefig('output/comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("완료! 결과는 'output' 폴더에 저장되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print("이미지 파일이 존재하는지 확인해 주세요.")

if __name__ == "__main__":
    simple_example()