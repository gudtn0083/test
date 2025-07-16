# 이미지 이진화 모듈 테스트

이 프로젝트의 이미지 이진화 모듈들에 대한 포괄적인 테스트 코드입니다.

## 📋 테스트 대상 모듈

- `simple_binary_converter.py` - 간단한 이진화 변환기
- `binary_image_converter.py` - 고급 이진화 변환기

## 🧪 테스트 구성

### 1. TestSimpleBinaryConverter
- 기본 이진화 함수 테스트
- 잘못된 입력에 대한 예외 처리 테스트
- 이미지 크기 일관성 테스트

### 2. TestBinaryImageConverter
- Otsu, 적응형, 단순 임계값 방법 테스트
- 이미지 저장 기능 테스트
- 빠른 변환 함수 테스트
- 결과 표시 기능 테스트

### 3. TestIntegration
- 두 변환기 간의 결과 일관성 테스트
- 다양한 임계값에 대한 테스트

### 4. TestPerformance
- 대용량 이미지 처리 성능 테스트

## 🚀 실행 방법

### 방법 1: 테스트 실행 스크립트 사용 (권장)

```bash
# 기본 테스트 (빠른 실행)
python run_tests.py basic

# 전체 테스트
python run_tests.py full

# 대화형 선택
python run_tests.py
```

### 방법 2: 직접 테스트 실행

```bash
# 빠른 테스트만 실행
python test_binary_converters.py --quick

# 전체 테스트 실행
python test_binary_converters.py

# unittest 모듈로 실행
python -m unittest test_binary_converters.py -v
```

### 방법 3: 개별 테스트 클래스 실행

```bash
# 특정 테스트 클래스만 실행
python -m unittest test_binary_converters.TestSimpleBinaryConverter -v

# 특정 테스트 메서드만 실행
python -m unittest test_binary_converters.TestBinaryImageConverter.test_convert_to_binary_otsu -v
```

## 📦 필요한 패키지

테스트 실행 전에 다음 패키지들이 설치되어 있어야 합니다:

```bash
pip install opencv-python numpy matplotlib pillow
```

또는 requirements.txt가 있다면:

```bash
pip install -r requirements.txt
```

## 📊 테스트 결과 예시

```
=== 이미지 이진화 모듈 테스트 시작 ===

test_convert_image_to_binary_success (test_binary_converters.TestSimpleBinaryConverter) ... ok
test_convert_to_binary_otsu (test_binary_converters.TestBinaryImageConverter) ... ok
test_both_converters_consistency (test_binary_converters.TestIntegration) ... ok
test_large_image_processing (test_binary_converters.TestPerformance) ... ok

=== 테스트 결과 ===
총 테스트 수: 15
성공: 15
실패: 0
에러: 0

🎉 모든 테스트가 성공했습니다!
```

## 🔧 테스트 커스터마이징

### 테스트 이미지 변경
테스트에서 사용하는 이미지를 변경하려면 각 테스트 클래스의 `setUp()` 메서드를 수정하세요.

### 새로운 테스트 추가
새로운 테스트를 추가하려면:
1. 해당 테스트 클래스에 `test_` 접두사로 시작하는 메서드 추가
2. `unittest.TestCase`의 assertion 메서드들 사용

### 성능 테스트 조정
`TestPerformance` 클래스에서 이미지 크기나 시간 제한을 조정할 수 있습니다.

## 🐛 문제 해결

### 1. 모듈 import 오류
```
ImportError: No module named 'cv2'
```
**해결책**: OpenCV 설치 - `pip install opencv-python`

### 2. 이미지 파일 오류
```
ValueError: 이미지를 읽을 수 없습니다
```
**해결책**: 테스트용 이미지 파일이 올바른 위치에 있는지 확인

### 3. Display 관련 오류 (서버 환경)
```
No display found
```
**해결책**: matplotlib을 non-GUI 백엔드로 설정
```python
import matplotlib
matplotlib.use('Agg')
```

## 📝 테스트 추가 가이드

새로운 기능을 추가할 때는 반드시 해당 테스트도 함께 작성하세요:

1. **단위 테스트**: 개별 함수의 동작 확인
2. **통합 테스트**: 모듈 간의 상호작용 확인
3. **경계값 테스트**: 극단적인 입력값에 대한 처리 확인
4. **예외 테스트**: 오류 상황에 대한 적절한 처리 확인

## 📈 테스트 커버리지

현재 테스트는 다음 항목들을 커버합니다:
- ✅ 정상적인 이미지 변환
- ✅ 다양한 이진화 방법 (Otsu, 적응형, 단순)
- ✅ 파일 I/O 기능
- ✅ 예외 처리
- ✅ 성능 검증
- ✅ 결과 일관성

## 🤝 기여하기

테스트 개선사항이나 새로운 테스트 케이스가 있다면 언제든지 추가해주세요!