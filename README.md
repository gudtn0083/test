# 🐾 귀여운 동물 생성기 (Cute Animal Generator)

이 프로젝트는 원본 곰 이미지와 유사한 스타일로 다양한 귀여운 동물 캐릭터들을 생성하는 두 가지 버전을 제공합니다.

## 🌟 기능

- **HTML/CSS/JavaScript 버전**: 웹 브라우저에서 실행되는 인터랙티브한 동물 생성기
- **Python 버전**: matplotlib를 사용한 프로그래밍 가능한 동물 생성기
- **8가지 동물 지원**: 곰, 고양이, 강아지, 토끼, 여우, 판다, 돼지, 개구리
- **랜덤 생성**: 다양한 색상 변형과 함께 랜덤 동물 생성
- **저장 기능**: 생성된 이미지를 파일로 저장

## 🚀 사용법

### HTML 버전

1. `animal_generator.html` 파일을 웹 브라우저에서 열기
2. 원하는 동물 버튼 클릭하여 생성
3. "랜덤 생성!" 버튼으로 여러 동물 한번에 생성
4. 생성된 동물 카드 클릭하여 같은 종류 추가 생성
5. 키보드 단축키:
   - `R`: 랜덤 동물 생성
   - `C`: 모든 동물 지우기

### Python 버전

#### 설치

```bash
pip install -r requirements.txt
```

#### 실행

```python
from animal_generator import AnimalGenerator

# 생성기 초기화
generator = AnimalGenerator()

# 특정 동물 생성
fig, ax = generator.generate_animal('bear')
plt.show()

# 랜덤 동물들 생성 (6개)
fig, axes = generator.generate_random_animals(6)
plt.show()

# 모든 동물 보기
fig, axes = generator.show_all_animals()
plt.show()

# 대화형 모드 실행
generator.main()
```

#### 예제 코드

```python
import matplotlib.pyplot as plt
from animal_generator import AnimalGenerator

# 생성기 생성
generator = AnimalGenerator()

# 개별 동물들 생성
animals = ['bear', 'cat', 'dog', 'rabbit']
for animal in animals:
    fig, ax = generator.generate_animal(animal)
    plt.savefig(f'cute_{animal}.png', dpi=150, bbox_inches='tight')
    plt.show()

# 사용자 지정 색상으로 곰 생성
custom_colors = {
    'main': '#654321',
    'secondary': '#8B7355', 
    'inner': '#D2B48C'
}
fig, ax = generator.generate_animal('bear', colors=custom_colors)
plt.show()
```

## 🎨 지원 동물

| 동물 | 특징 |
|------|------|
| 🐻 곰 (bear) | 둥근 귀, 갈색 털 |
| 🐱 고양이 (cat) | 뾰족한 귀, 수염, 고양이 눈 |
| 🐶 강아지 (dog) | 늘어진 귀, 혀, 친근한 표정 |
| 🐰 토끼 (rabbit) | 긴 귀, 앞니, Y자 코 |
| 🦊 여우 (fox) | 뾰족한 얼굴, 호박색 눈 |
| 🐼 판다 (panda) | 검은 눈 주위, 흑백 색상 |
| 🐷 돼지 (pig) | 분홍색, 큰 코 |
| 🐸 개구리 (frog) | 튀어나온 눈, 큰 입 |

## 🛠️ 커스터마이징

### HTML 버전
- CSS 스타일 수정으로 UI 테마 변경 가능
- JavaScript에서 색상 팔레트 수정으로 다양한 색상 조합 추가
- 새로운 동물 템플릿 추가 가능

### Python 버전
- `colors` 파라미터로 사용자 지정 색상 적용
- 새로운 동물 생성 함수 추가하여 동물 종류 확장
- matplotlib 스타일 변경으로 다른 그래픽 스타일 적용

## 📁 파일 구조

```
animal-generator/
├── animal_generator.html    # 웹 버전 (HTML/CSS/JS)
├── animal_generator.py      # Python 버전
├── requirements.txt         # Python 의존성
└── README.md               # 사용 설명서
```

## 🎯 활용 예시

- 어린이용 교육 콘텐츠
- 웹사이트 캐릭터/아바타
- 게임 캐릭터 프로토타입
- 일러스트레이션 참고자료
- 프로그래밍 학습용 예제

## 📄 라이선스

이 프로젝트는 자유롭게 사용, 수정, 배포할 수 있습니다.

## 🤝 기여

새로운 동물 추가, 버그 수정, 기능 개선에 대한 기여를 환영합니다!

---

즐거운 동물 생성을 해보세요! 🐾✨