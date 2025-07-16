# 한국어 텍스트 추출 도구
## Korean Text Extraction Tool

이 도구는 이미지에서 한국어와 영어 텍스트를 추출하는 OCR(Optical Character Recognition) 프로그램입니다.

## 🚀 빠른 시작

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 간단한 사용법

```bash
python simple_text_extractor.py
```

### 3. 고급 사용법

```bash
# 기본 사용 (모든 OCR 엔진 사용)
python text_extractor.py image.png

# 특정 OCR 엔진만 사용
python text_extractor.py image.png --engines easyocr

# 결과를 파일로 저장
python text_extractor.py image.png --output result.txt
```

## 📋 지원하는 OCR 엔진

### 1. EasyOCR (추천)
- **장점**: 한국어 인식 정확도가 높음, 설치 및 사용이 간단
- **단점**: 초기 모델 다운로드 시간이 다소 소요
- **설치**: `pip install easyocr`

### 2. Tesseract OCR
- **장점**: 전통적인 OCR 엔진, 다양한 언어 지원
- **단점**: 별도 설치 필요, 전처리가 중요
- **설치**: 
  - Windows: [Tesseract 설치](https://github.com/UB-Mannheim/tesseract/wiki)
  - Ubuntu: `sudo apt install tesseract-ocr tesseract-ocr-kor`
  - macOS: `brew install tesseract tesseract-lang`

### 3. PaddleOCR
- **장점**: 높은 성능, 다양한 언어 지원
- **단점**: 설치 패키지가 큼
- **설치**: `pip install paddlepaddle paddleocr`

## 📁 파일 설명

- `simple_text_extractor.py`: 간단한 대화형 텍스트 추출 도구
- `text_extractor.py`: 고급 기능을 포함한 완전한 텍스트 추출 도구
- `requirements.txt`: 필요한 Python 패키지 목록

## 💡 사용 예제

### 간단한 사용법
```python
from simple_text_extractor import extract_text_simple

# 이미지에서 텍스트 추출
text = extract_text_simple("image.png")
print(text)
```

### 고급 사용법
```python
from text_extractor import TextExtractor

# 텍스트 추출기 생성
extractor = TextExtractor()

# 모든 OCR 엔진으로 텍스트 추출
results = extractor.extract_text("image.png")

# 결과 출력
for engine, result in results.items():
    print(f"{result['engine']}: {result['full_text']}")
```

## 🔧 문제 해결

### 1. EasyOCR 설치 오류
```bash
pip install --upgrade pip
pip install easyocr
```

### 2. Tesseract 언어 팩 오류
```bash
# Ubuntu
sudo apt install tesseract-ocr-kor

# 또는 언어 코드 확인
tesseract --list-langs
```

### 3. GPU 사용 (선택사항)
```bash
# CUDA 지원 버전 설치 (GPU 가속)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📸 지원하는 이미지 형식

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## ⚙️ 성능 최적화 팁

1. **이미지 품질**: 높은 해상도와 대비가 좋은 이미지 사용
2. **전처리**: 노이즈 제거, 이진화 등의 전처리로 인식률 향상
3. **OCR 엔진 선택**: 
   - 한국어 텍스트: EasyOCR 추천
   - 영어 텍스트: Tesseract 추천
   - 혼합 텍스트: 여러 엔진 비교 후 선택

## 🐛 알려진 문제

1. 손글씨 인식률은 제한적임
2. 기울어진 텍스트의 경우 전처리가 필요할 수 있음
3. 매우 작은 글씨는 인식이 어려울 수 있음

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트 등 모든 기여를 환영합니다!

## 📞 문의

문제가 있거나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.