# 음성 파일 인식 시스템

한국어와 다양한 언어의 음성 파일을 텍스트로 변환하는 파이썬 기반 음성 인식 시스템입니다.

## 기능

- **다양한 오디오 형식 지원**: WAV, MP3, MP4, M4A, FLAC, AAC, OGG, WMA
- **온라인/오프라인 음성 인식**: Google Speech API 및 PocketSphinx 지원
- **다국어 지원**: 한국어, 영어, 일본어, 중국어 등
- **일괄 처리**: 디렉토리 내 모든 오디오 파일 자동 처리
- **결과 저장**: 인식 결과를 텍스트 파일로 저장
- **명령줄 인터페이스**: 스크립트 실행 또는 대화형 사용 가능

## 설치

### 1. 자동 설치 (권장)
```bash
python setup.py
```

### 2. 수동 설치

#### 시스템 의존성 설치

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip ffmpeg portaudio19-dev python3-pyaudio flac libespeak-dev swig libpulse-dev
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum update -y
sudo yum install -y python3-pip ffmpeg portaudio-devel flac espeak-devel swig pulseaudio-libs-devel
```

**macOS:**
```bash
brew install ffmpeg portaudio flac swig
```

#### Python 패키지 설치
```bash
pip install -r requirements.txt
```

## 사용법

### 1. 인터랙티브 모드
```bash
python speech_recognition_system.py
```

### 2. 명령줄 사용

#### 단일 파일 처리
```bash
# 한국어 음성 인식
python speech_recognition_system.py audio_file.wav

# 영어 음성 인식
python speech_recognition_system.py audio_file.wav --language en-US

# 오프라인 인식
python speech_recognition_system.py audio_file.wav --method offline

# 결과 파일 저장
python speech_recognition_system.py audio_file.wav --output result.txt
```

#### 일괄 처리
```bash
# 디렉토리 내 모든 오디오 파일 처리
python speech_recognition_system.py audio_files --batch

# 결과를 파일로 저장
python speech_recognition_system.py audio_files --batch --output batch_results.txt
```

### 3. 프로그래밍 사용
```python
from speech_recognition_system import SpeechRecognitionSystem

# 시스템 초기화
srs = SpeechRecognitionSystem()

# 단일 파일 처리
result = srs.process_audio_file("audio_file.wav", method="google", language="ko-KR")
print(result)

# 일괄 처리
results = srs.batch_process("audio_files", "results.txt")
```

## 지원 언어

### 주요 언어 코드
- **한국어**: `ko-KR`
- **영어**: `en-US` (미국), `en-GB` (영국)
- **일본어**: `ja-JP`
- **중국어**: `zh-CN` (간체), `zh-TW` (번체)
- **스페인어**: `es-ES`
- **프랑스어**: `fr-FR`
- **독일어**: `de-DE`
- **러시아어**: `ru-RU`

## 파일 구조

```
├── speech_recognition_system.py  # 메인 시스템
├── example_usage.py             # 사용 예제
├── setup.py                     # 설치 스크립트
├── requirements.txt             # 의존성 패키지
├── README.md                    # 사용 설명서
└── audio_files/                 # 오디오 파일 저장소
    └── README.txt
```

## 예제

### 예제 1: 한국어 음성 인식
```python
from speech_recognition_system import SpeechRecognitionSystem

srs = SpeechRecognitionSystem()
result = srs.process_audio_file("korean_speech.wav", language="ko-KR")
print(f"인식 결과: {result}")
```

### 예제 2: 영어 음성 인식
```python
result = srs.process_audio_file("english_speech.mp3", language="en-US")
print(f"Recognition result: {result}")
```

### 예제 3: 일괄 처리
```python
results = srs.batch_process("./audio_files", "recognition_results.txt")
print(f"처리된 파일 수: {len(results)}")
```

## 성능 최적화

### 1. 오디오 품질 개선
- 샘플링 레이트: 16kHz 이상 권장
- 비트 깊이: 16bit 이상
- 잡음 제거: 사전에 오디오 편집 소프트웨어로 처리

### 2. 인식 정확도 향상
- 명확한 발음과 적절한 음량
- 배경 잡음 최소화
- 짧은 구간으로 분할하여 처리

## 트러블슈팅

### 1. 설치 관련 문제

**PyAudio 설치 오류:**
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# macOS
brew install portaudio
```

**FFmpeg 관련 오류:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### 2. 인식 관련 문제

**"음성을 인식할 수 없습니다" 오류:**
- 오디오 파일 품질 확인
- 음성이 너무 짧거나 긴 경우
- 언어 설정 확인

**Google API 오류:**
- 인터넷 연결 확인
- 너무 많은 요청으로 인한 제한
- 오프라인 모드(`--method offline`) 사용

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

버그 리포트, 기능 제안, 코드 기여를 환영합니다.

## 주의사항

1. Google Speech Recognition API는 인터넷 연결이 필요합니다
2. 오프라인 인식(PocketSphinx)은 정확도가 상대적으로 낮습니다
3. 긴 오디오 파일은 메모리 사용량이 많을 수 있습니다
4. 상업적 사용 시 Google API 정책을 확인하세요