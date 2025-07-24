# 🐾 귀여운 동물 AI 이미지 생성기 (보안 강화 버전)

AI를 사용하여 세상에서 가장 귀여운 동물 이미지들을 안전하게 자동 생성하는 도구입니다! 🎨✨🔒

## 🌟 주요 기능

- 🤖 **최신 AI 기술**: Stable Diffusion을 활용한 고품질 이미지 생성
- 🐾 **다양한 동물**: 강아지, 고양이, 아기 판다 등 18종류의 귀여운 동물들
- 🎨 **다양한 스타일**: 카와이, 치비, 픽사, 디즈니 등 8가지 아트 스타일
- 🌈 **자동 귀여움 향상**: AI가 생성한 이미지를 더욱 귀엽게 만드는 후처리
- 💻 **웹 인터페이스**: 사용하기 쉬운 Streamlit 기반 웹앱
- ⌨️ **명령행 도구**: 개발자를 위한 CLI 인터페이스
- 🎪 **배치 생성**: 여러 이미지를 한번에 생성
- 🔒 **보안 강화**: 입력 검증, 접근 제어, 안전한 파일 처리

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 레포지토리 클론
git clone <repository-url>
cd cute-animal-generator

# 의존성 설치
pip install -r requirements.txt
```

### 2. 웹 인터페이스 실행

```bash
# 웹앱 실행
streamlit run web_app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용하세요!

### 3. 명령행에서 빠른 생성

```bash
# 기본 사용법
python cli_generator.py --animal puppy

# 고화질 이미지 생성
python cli_generator.py --animal "baby panda" --size 1024 --steps 30

# 커스텀 프롬프트 사용
python cli_generator.py --prompt "cute kitten with rainbow background, kawaii style"

# 여러 동물 배치 생성
python cli_generator.py --batch --count 5 --animals puppy kitten "baby fox"
```

## 📖 상세 사용법

### 웹 인터페이스 사용법

1. **동물 선택**: 사이드바에서 원하는 동물을 선택하거나 랜덤으로 설정
2. **스타일 설정**: 카와이, 치비, 픽사 등 원하는 아트 스타일 선택
3. **고급 설정**: 이미지 크기, 생성 품질, 창의성 수준 조절
4. **커스텀 프롬프트**: 더 구체적인 설명으로 원하는 이미지 생성
5. **생성 및 다운로드**: 버튼을 클릭하여 이미지 생성 후 다운로드

### 명령행 인터페이스 사용법

#### 기본 명령어

```bash
# 도움말 보기
python cli_generator.py --help

# 사용 가능한 동물 목록 보기
python cli_generator.py --list-animals

# 기본 이미지 생성
python cli_generator.py --animal puppy --output my_puppy.png
```

#### 고급 옵션

```bash
# 스타일과 크기 지정
python cli_generator.py --animal kitten --style kawaii --size 768

# 높은 품질 설정
python cli_generator.py --animal "baby panda" --steps 50 --guidance 10

# 랜덤 동물 생성
python cli_generator.py --random --output random_animal.png
```

#### 배치 생성

```bash
# 4마리 랜덤 동물 생성
python cli_generator.py --batch --count 4

# 특정 동물들로 배치 생성
python cli_generator.py --batch --animals puppy kitten "baby panda" --output-dir my_animals
```

### Python 코드에서 사용하기

```python
from cute_animal_generator import CuteAnimalGenerator, quick_generate

# 빠른 생성 (한 줄로!)
image = quick_generate(animal="puppy", save_as="my_puppy.png")

# 고급 사용법
generator = CuteAnimalGenerator()

# 단일 이미지 생성
images = generator.generate_image(
    animal="kitten",
    width=768,
    height=768,
    num_inference_steps=30
)

# 귀여움 향상 후처리
enhanced_image = generator.enhance_cuteness(images[0])
final_image = generator.add_cute_effects(enhanced_image)
final_image.save("super_cute_kitten.png")

# 배치 생성
batch_images = generator.generate_cute_animal_batch(
    count=5,
    animals=["puppy", "kitten", "baby panda"],
    save_path="animal_collection"
)
```

## 🐾 사용 가능한 동물들

- 🐶 **강아지** (puppy)
- 🐱 **고양이** (kitten)
- 🐼 **아기 판다** (baby panda)
- 🦊 **아기 여우** (baby fox)
- 🐰 **아기 토끼** (baby rabbit)
- 🐻 **아기 곰** (baby bear)
- 🐘 **아기 코끼리** (baby elephant)
- 🐧 **아기 펭귄** (baby penguin)
- 🦉 **아기 부엉이** (baby owl)
- 🦌 **아기 사슴** (baby deer)
- 🦭 **아기 물개** (baby seal)
- 🦔 **아기 고슴도치** (baby hedgehog)
- 🦝 **아기 라쿤** (baby raccoon)
- 🐨 **아기 코알라** (baby koala)
- 🐅 **아기 호랑이** (baby tiger)
- 🦁 **아기 사자** (baby lion)
- 🐹 **햄스터** (hamster)
- 🐭 **기니피그** (guinea pig)

## 🎨 지원 스타일

- **카와이 스타일** (kawaii): 일본식 귀여운 스타일
- **치비 스타일** (chibi): 작고 동글동글한 캐릭터 스타일
- **만화 스타일** (cartoon): 서양식 만화 스타일
- **애니메이션 스타일** (anime): 일본 애니메이션 스타일
- **픽사 스타일** (pixar): 3D 애니메이션 스타일
- **디즈니 스타일** (disney): 클래식 디즈니 스타일
- **지브리 스타일** (ghibli): 스튜디오 지브리 스타일

## ⚙️ 시스템 요구사항

- **Python**: 3.8 이상
- **GPU**: CUDA 지원 GPU 권장 (없어도 CPU로 동작)
- **메모리**: 최소 8GB RAM (16GB 권장)
- **저장공간**: 최소 10GB (모델 파일 포함)

## 🛠️ 기술 스택

- **AI 모델**: Stable Diffusion 1.5
- **딥러닝 프레임워크**: PyTorch
- **이미지 생성**: Diffusers
- **웹 인터페이스**: Streamlit
- **이미지 처리**: PIL, OpenCV
- **UI/UX**: 커스텀 CSS

## 💡 생성 팁

### 더 귀여운 결과를 얻으려면:

1. **키워드 활용**: "big eyes", "fluffy", "adorable", "soft" 등의 단어 추가
2. **색상 지정**: "pastel colors", "pink", "rainbow" 등으로 색감 조절
3. **배경 설정**: "in garden", "with flowers", "on clouds" 등으로 분위기 연출
4. **액세서리**: "wearing hat", "with bow tie", "flower crown" 등으로 포인트 추가

### 품질 향상 방법:

1. **생성 스텝 증가**: 20 → 30 → 50 (시간은 오래 걸리지만 품질 향상)
2. **가이던스 스케일 조절**: 7.5가 기본, 높이면 프롬프트를 더 잘 따름
3. **고해상도 생성**: 512 → 768 → 1024 (더 선명한 이미지)

## 🔒 보안 기능

### 입력 보안
- **프롬프트 정화**: 악성 스크립트 및 위험한 패턴 자동 제거
- **파일명 검증**: 경로 탐색 공격 방지 및 안전한 문자만 허용
- **파라미터 제한**: 안전한 범위 내에서만 이미지 생성 가능

### 접근 제어
- **화이트리스트**: 허용된 동물과 스타일만 선택 가능
- **요청 제한**: 시간당/일일 생성 횟수 제한으로 남용 방지
- **세션 관리**: 자동 타임아웃 및 보안 세션 관리

### 시스템 보안
- **메모리 관리**: 자동 캐시 정리 및 메모리 누수 방지
- **로깅**: 모든 보안 이벤트 및 사용자 활동 기록
- **오류 처리**: 민감한 정보 노출 방지

자세한 보안 정보는 [SECURITY.md](SECURITY.md)를 참조하세요.

## 🚨 주의사항

- **첫 실행**: 최초 실행시 AI 모델을 다운로드하므로 시간이 걸릴 수 있습니다
- **GPU 메모리**: 고해상도 이미지 생성시 GPU 메모리 부족이 발생할 수 있습니다
- **생성 시간**: 이미지 크기와 품질 설정에 따라 생성 시간이 달라집니다
- **보안 정책**: 부적절한 내용 입력시 자동으로 차단됩니다
- **사용 제한**: 과도한 사용 방지를 위한 일일 생성 횟수 제한이 있습니다

## 🤝 기여하기

이 프로젝트에 기여하고 싶으시다면:

1. 이슈를 생성하여 버그 리포트나 기능 제안
2. Pull Request를 통한 코드 기여
3. 새로운 동물이나 스타일 추가 제안

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙏 감사의 말

- Stability AI의 Stable Diffusion 모델
- Hugging Face의 Diffusers 라이브러리
- Streamlit 커뮤니티

---

**🎉 귀여운 동물 친구들과 함께 즐거운 시간 보내세요! 🐾**