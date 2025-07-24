# 노래방 기계 (Karaoke Machine)

웹 기반 노래방 애플리케이션입니다. 노래 검색, 예약, 인기 차트 등의 기능을 제공합니다.

## 주요 기능

- 🎤 **노래 검색 및 필터링**: 제목, 가수명으로 검색하고 장르별로 필터링
- 📊 **인기 차트**: 재생 횟수 기반 인기 노래 순위
- 📋 **예약 시스템**: 노래 예약 대기열 관리
- 🎵 **노래 관리**: 관리자 모드에서 새로운 노래 추가
- 📱 **반응형 디자인**: 모바일 및 태블릿 지원

## 기술 스택

### Backend
- Node.js
- Express.js
- SQLite3 (데이터베이스)
- Multer (파일 업로드)

### Frontend
- HTML5
- CSS3 (반응형 디자인)
- Vanilla JavaScript
- Font Awesome (아이콘)

## 설치 및 실행

1. 의존성 설치:
```bash
npm install
```

2. 서버 실행:
```bash
npm start
```

3. 개발 모드 실행 (nodemon 사용):
```bash
npm run dev
```

4. 브라우저에서 접속:
```
http://localhost:3000
```

## 프로젝트 구조

```
karaoke-machine/
├── server.js           # Express 서버 및 API
├── package.json        # 프로젝트 설정 및 의존성
├── karaoke.db         # SQLite 데이터베이스 (자동 생성)
├── public/            # 정적 파일
│   ├── index.html     # 메인 HTML
│   ├── style.css      # 스타일시트
│   └── app.js         # 프론트엔드 JavaScript
└── uploads/           # 업로드된 파일 (자동 생성)
    ├── songs/         # 노래 파일
    └── lyrics/        # 가사 파일
```

## API 엔드포인트

### 노래 관련
- `GET /api/songs` - 모든 노래 조회 (검색, 필터 지원)
- `GET /api/songs/:id` - 특정 노래 조회
- `POST /api/songs` - 새 노래 추가 (파일 업로드 포함)
- `GET /api/popular` - 인기 차트 조회

### 예약 관련
- `GET /api/queue` - 예약 대기열 조회
- `POST /api/queue` - 예약 추가
- `DELETE /api/queue/:id` - 예약 취소

### 재생 관련
- `POST /api/play/:id` - 노래 재생 시작 (재생 횟수 증가)

## 사용 방법

### 노래 검색 및 예약
1. 메인 화면에서 노래를 검색하거나 장르별로 필터링
2. 원하는 노래를 클릭하여 예약 모달 열기
3. 이름을 입력하고 예약하기 버튼 클릭
4. 예약 대기열 탭에서 예약 상태 확인

### 노래 추가 (관리자)
1. 우측 상단의 관리자 버튼 클릭
2. 노래 정보 입력 (제목, 가수, 장르 등)
3. 노래 파일과 가사 파일 선택 (선택사항)
4. 노래 추가 버튼 클릭

## 데이터베이스 스키마

### songs 테이블
- `id`: 고유 ID
- `title`: 노래 제목
- `artist`: 가수명
- `genre`: 장르
- `year`: 발매년도
- `song_file`: 노래 파일명
- `lyrics_file`: 가사 파일명
- `duration`: 재생 시간 (초)
- `play_count`: 재생 횟수
- `created_at`: 생성 시간

### queue 테이블
- `id`: 고유 ID
- `song_id`: 노래 ID (외래키)
- `user_name`: 예약자 이름
- `created_at`: 예약 시간
- `status`: 상태 ('waiting', 'playing')

## 향후 개선 사항

- [ ] 실제 오디오 플레이어 통합
- [ ] 가사 동기화 표시 (LRC 파일 지원)
- [ ] 사용자 인증 및 권한 관리
- [ ] 노래 평점 및 리뷰 기능
- [ ] 실시간 업데이트 (WebSocket)
- [ ] 노래 추천 시스템
- [ ] 다국어 지원

## 라이선스

MIT License