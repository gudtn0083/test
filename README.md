# 이미지 윤곽선 추출 도구

이 도구는 이미지에서 윤곽선만 추출하는 다양한 알고리즘을 제공합니다. OpenCV를 기반으로 구현되었으며, 5가지 서로 다른 윤곽선 검출 방법을 지원합니다.

## 🔧 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 🚀 사용 방법

### 1. 간단한 예제 실행

```bash
python simple_edge_example.py
```

이 명령은 `Test1.PNG` 파일을 사용하여 윤곽선을 추출하고 결과를 `output` 폴더에 저장합니다.

### 2. 명령행 인터페이스 사용

#### 모든 방법으로 윤곽선 추출:
```bash
python edge_detector.py --image Test1.PNG --output output --method all
```

#### 특정 방법만 사용:
```bash
# Canny Edge Detection만 사용
python edge_detector.py --image Test1.PNG --method canny

# Sobel Edge Detection만 사용
python edge_detector.py --image Test1.PNG --method sobel
```

#### 결과를 화면에 표시:
```bash
python edge_detector.py --image Test1.PNG --display
```

### 3. Python 코드에서 직접 사용

```python
from edge_detector import EdgeDetector

# EdgeDetector 객체 생성
detector = EdgeDetector("your_image.jpg")

# Canny edge detection 적용
canny_edges = detector.canny_edge_detection()

# 모든 방법 적용하고 저장
detector.save_results("output_folder")

# 결과 화면에 표시
detector.display_results()
```

## 📊 지원하는 윤곽선 추출 방법

### 1. **Canny Edge Detection**
- 가장 널리 사용되는 윤곽선 검출 알고리즘
- 노이즈에 강하고 얇은 윤곽선을 생성
- 매개변수: `low_threshold`, `high_threshold`, `blur_ksize`

### 2. **Sobel Edge Detection**
- X, Y 방향의 gradient를 계산하여 윤곽선 검출
- 방향성 정보를 제공
- 빠른 처리 속도

### 3. **Laplacian Edge Detection**
- 2차 미분을 사용한 윤곽선 검출
- 모든 방향의 윤곽선을 검출
- 노이즈에 민감

### 4. **Adaptive Threshold**
- 적응형 임계값을 사용한 윤곽선 추출
- 조명 조건이 불균등한 이미지에 효과적
- 지역적 특성을 고려

### 5. **Morphological Edge Detection**
- 형태학적 연산(침식, 팽창)을 사용
- 이진 이미지에서 윤곽선 추출
- 객체의 경계를 명확하게 표현

## 📁 출력 파일

실행 후 `output` 폴더에 다음 파일들이 생성됩니다:

- `original.png`: 원본 이미지
- `canny_edges.png`: Canny edge detection 결과
- `sobel_edges.png`: Sobel edge detection 결과
- `laplacian_edges.png`: Laplacian edge detection 결과
- `adaptive_edges.png`: Adaptive threshold 결과
- `morphological_edges.png`: Morphological edge detection 결과
- `comparison.png`: 여러 방법의 비교 결과 (simple_edge_example.py 실행 시)

## ⚙️ 매개변수 조정

각 방법의 매개변수를 조정하여 더 나은 결과를 얻을 수 있습니다:

```python
# Canny 매개변수 조정
canny_edges = detector.canny_edge_detection(
    low_threshold=30,    # 낮은 임계값 (기본값: 50)
    high_threshold=100,  # 높은 임계값 (기본값: 150)
    blur_ksize=3        # 블러 커널 크기 (기본값: 5)
)
```

## 💡 사용 팁

1. **이미지 품질**: 고해상도 이미지일수록 더 정확한 윤곽선을 얻을 수 있습니다.
2. **방법 선택**: 
   - 일반적인 용도: Canny Edge Detection
   - 빠른 처리: Sobel Edge Detection
   - 불균등한 조명: Adaptive Threshold
3. **매개변수 조정**: 각 이미지의 특성에 맞게 임계값을 조정하세요.

## 🐛 문제 해결

### 이미지를 불러올 수 없는 경우:
- 이미지 파일 경로가 올바른지 확인
- 지원하는 이미지 형식인지 확인 (PNG, JPG, JPEG, BMP 등)

### 메모리 오류가 발생하는 경우:
- 이미지 크기를 줄여서 시도
- 한 번에 하나의 방법만 실행

## 📋 요구사항

- Python 3.7+
- OpenCV 4.x
- NumPy
- Matplotlib
- Pillow

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.