import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import argparse

class EdgeDetector:
    """이미지에서 윤곽선을 추출하는 클래스"""
    
    def __init__(self, image_path):
        """
        이미지 경로를 받아 EdgeDetector 객체를 초기화합니다.
        
        Args:
            image_path (str): 처리할 이미지 파일 경로
        """
        self.image_path = image_path
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError(f"이미지를 로드할 수 없습니다: {image_path}")
        
        # 그레이스케일로 변환
        self.gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
    def canny_edge_detection(self, low_threshold=50, high_threshold=150, blur_ksize=5):
        """
        Canny edge detection을 사용한 윤곽선 추출
        
        Args:
            low_threshold (int): Canny 하위 임계값
            high_threshold (int): Canny 상위 임계값
            blur_ksize (int): 가우시안 블러 커널 크기
            
        Returns:
            numpy.ndarray: 윤곽선이 추출된 이미지
        """
        # 노이즈 제거를 위한 가우시안 블러 적용
        blurred = cv2.GaussianBlur(self.gray_image, (blur_ksize, blur_ksize), 0)
        
        # Canny edge detection 적용
        edges = cv2.Canny(blurred, low_threshold, high_threshold)
        
        return edges
    
    def sobel_edge_detection(self):
        """
        Sobel operator를 사용한 윤곽선 추출
        
        Returns:
            numpy.ndarray: 윤곽선이 추출된 이미지
        """
        # Sobel X와 Y 방향 gradient 계산
        sobel_x = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(self.gray_image, cv2.CV_64F, 0, 1, ksize=3)
        
        # 두 방향의 gradient를 결합
        sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # 0-255 범위로 정규화
        sobel_normalized = np.uint8(sobel_combined / np.max(sobel_combined) * 255)
        
        return sobel_normalized
    
    def laplacian_edge_detection(self):
        """
        Laplacian operator를 사용한 윤곽선 추출
        
        Returns:
            numpy.ndarray: 윤곽선이 추출된 이미지
        """
        # 노이즈 제거를 위한 가우시안 블러 적용
        blurred = cv2.GaussianBlur(self.gray_image, (3, 3), 0)
        
        # Laplacian edge detection 적용
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
        
        # 절댓값을 취하고 정규화
        laplacian = np.uint8(np.absolute(laplacian))
        
        return laplacian
    
    def adaptive_threshold_edges(self):
        """
        적응형 임계값을 사용한 윤곽선 추출
        
        Returns:
            numpy.ndarray: 윤곽선이 추출된 이미지
        """
        # 가우시안 블러 적용
        blurred = cv2.GaussianBlur(self.gray_image, (5, 5), 0)
        
        # 적응형 임계값 적용
        adaptive_thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 반전하여 검은 배경에 흰 윤곽선으로 만들기
        return cv2.bitwise_not(adaptive_thresh)
    
    def morphological_edges(self):
        """
        형태학적 연산을 사용한 윤곽선 추출
        
        Returns:
            numpy.ndarray: 윤곽선이 추출된 이미지
        """
        # 이진화
        _, binary = cv2.threshold(self.gray_image, 127, 255, cv2.THRESH_BINARY)
        
        # 모폴로지 커널 생성
        kernel = np.ones((3, 3), np.uint8)
        
        # 침식과 팽창을 통한 윤곽선 추출
        erosion = cv2.erode(binary, kernel, iterations=1)
        dilation = cv2.dilate(binary, kernel, iterations=1)
        
        # 차이를 계산하여 윤곽선 추출
        edges = cv2.absdiff(dilation, erosion)
        
        return edges
    
    def process_all_methods(self):
        """
        모든 윤곽선 추출 방법을 적용하고 결과를 반환
        
        Returns:
            dict: 각 방법별 결과 이미지들
        """
        results = {
            'original': cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB),
            'canny': self.canny_edge_detection(),
            'sobel': self.sobel_edge_detection(),
            'laplacian': self.laplacian_edge_detection(),
            'adaptive': self.adaptive_threshold_edges(),
            'morphological': self.morphological_edges()
        }
        
        return results
    
    def save_results(self, output_dir='output'):
        """
        모든 결과를 파일로 저장
        
        Args:
            output_dir (str): 결과를 저장할 디렉토리
        """
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        results = self.process_all_methods()
        
        for method_name, result_image in results.items():
            if method_name == 'original':
                # 원본 이미지는 BGR을 RGB로 변환하여 저장
                output_path = os.path.join(output_dir, f'{method_name}.png')
                plt.imsave(output_path, result_image)
            else:
                # 윤곽선 이미지는 그레이스케일로 저장
                output_path = os.path.join(output_dir, f'{method_name}_edges.png')
                cv2.imwrite(output_path, result_image)
        
        print(f"모든 결과가 '{output_dir}' 디렉토리에 저장되었습니다.")
    
    def display_results(self):
        """
        모든 결과를 matplotlib를 사용해 시각화
        """
        results = self.process_all_methods()
        
        # 플롯 설정
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('이미지 윤곽선 추출 결과', fontsize=16)
        
        # 각 결과 표시
        titles = ['원본 이미지', 'Canny Edge', 'Sobel Edge', 
                 'Laplacian Edge', 'Adaptive Threshold', 'Morphological Edge']
        
        for i, (method_name, title) in enumerate(zip(results.keys(), titles)):
            row = i // 3
            col = i % 3
            
            if method_name == 'original':
                axes[row, col].imshow(results[method_name])
            else:
                axes[row, col].imshow(results[method_name], cmap='gray')
            
            axes[row, col].set_title(title)
            axes[row, col].axis('off')
        
        plt.tight_layout()
        plt.show()

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='이미지 윤곽선 추출 도구')
    parser.add_argument('--image', type=str, default='Test1.PNG', 
                       help='처리할 이미지 파일 경로')
    parser.add_argument('--output', type=str, default='output', 
                       help='결과를 저장할 디렉토리')
    parser.add_argument('--method', type=str, choices=['canny', 'sobel', 'laplacian', 'adaptive', 'morphological', 'all'], 
                       default='all', help='사용할 윤곽선 추출 방법')
    parser.add_argument('--display', action='store_true', 
                       help='결과를 화면에 표시')
    
    args = parser.parse_args()
    
    try:
        # EdgeDetector 객체 생성
        detector = EdgeDetector(args.image)
        
        if args.method == 'all':
            # 모든 방법 적용하고 저장
            detector.save_results(args.output)
            
            if args.display:
                detector.display_results()
        else:
            # 특정 방법만 적용
            if args.method == 'canny':
                result = detector.canny_edge_detection()
            elif args.method == 'sobel':
                result = detector.sobel_edge_detection()
            elif args.method == 'laplacian':
                result = detector.laplacian_edge_detection()
            elif args.method == 'adaptive':
                result = detector.adaptive_threshold_edges()
            elif args.method == 'morphological':
                result = detector.morphological_edges()
            
            # 결과 저장
            os.makedirs(args.output, exist_ok=True)
            output_path = os.path.join(args.output, f'{args.method}_edges.png')
            cv2.imwrite(output_path, result)
            print(f"결과가 '{output_path}'에 저장되었습니다.")
            
            if args.display:
                plt.figure(figsize=(12, 6))
                
                plt.subplot(1, 2, 1)
                plt.imshow(cv2.cvtColor(detector.original_image, cv2.COLOR_BGR2RGB))
                plt.title('원본 이미지')
                plt.axis('off')
                
                plt.subplot(1, 2, 2)
                plt.imshow(result, cmap='gray')
                plt.title(f'{args.method.capitalize()} Edge Detection')
                plt.axis('off')
                
                plt.tight_layout()
                plt.show()
    
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()