# 파일 전송 시스템

이 프로젝트는 다양한 방법으로 파일을 전송할 수 있는 Python 기반 시스템입니다.

## 🚀 기능

1. **HTTP 기반 파일 전송** - 웹 브라우저를 통한 파일 업로드/다운로드
2. **소켓 기반 파일 전송** - TCP 소켓을 이용한 직접 파일 전송
3. **클라이언트 API** - 프로그래밍 방식으로 파일 전송

## 📦 설치

필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

## 🌐 HTTP 기반 파일 전송

### 서버 실행

```bash
python file_transfer_http_server.py
```

- 웹 브라우저에서 `http://localhost:5000` 접속
- 브라우저를 통해 파일 업로드/다운로드 가능

### 클라이언트 사용

```bash
python file_transfer_client.py
```

대화형 메뉴를 통해:
- 파일 업로드
- 파일 다운로드  
- 서버 파일 목록 확인

## 🔌 소켓 기반 파일 전송

### 서버 실행

```bash
python file_transfer_socket.py
```

메뉴에서 "1. 서버 실행" 선택

### 클라이언트 실행

```bash
python file_transfer_socket.py
```

메뉴에서 "2. 클라이언트 실행" 선택

## 📋 지원 기능

### HTTP 서버 기능
- ✅ 웹 브라우저 UI
- ✅ 다중 파일 업로드
- ✅ 파일 다운로드
- ✅ 파일 목록 조회
- ✅ 중복 파일명 자동 처리
- ✅ 파일 크기 제한 (100MB)
- ✅ 보안 파일명 처리

### 소켓 서버 기능
- ✅ TCP 소켓 통신
- ✅ 다중 클라이언트 지원
- ✅ 진행률 표시
- ✅ 중복 파일명 처리
- ✅ 바이너리 파일 지원

### 클라이언트 기능
- ✅ 대화형 메뉴
- ✅ 오류 처리
- ✅ 연결 상태 확인
- ✅ 한국어 인터페이스

## 🔧 설정

### HTTP 서버 설정
- 포트: 5000
- 업로드 폴더: `uploads/`
- 최대 파일 크기: 100MB

### 소켓 서버 설정  
- 포트: 9999
- 업로드 폴더: `socket_uploads/`
- 버퍼 크기: 4096 bytes

## 🛡️ 보안 주의사항

1. **파일 검증**: 업로드되는 파일의 확장자와 내용을 검증하세요
2. **접근 제어**: 프로덕션 환경에서는 인증/인가 시스템을 구현하세요
3. **네트워크 보안**: HTTPS 및 암호화를 사용하세요
4. **파일 크기 제한**: 적절한 파일 크기 제한을 설정하세요

## 🐛 문제 해결

### 포트 충돌
```bash
# 다른 포트 사용
python file_transfer_http_server.py --port 8080
```

### 권한 문제
```bash
# 폴더 권한 확인
chmod 755 uploads/
chmod 755 socket_uploads/
```

### 방화벽 설정
서버 포트(5000, 9999)가 방화벽에서 허용되어 있는지 확인하세요.

## 📝 예제 사용법

### Python 스크립트에서 사용

```python
from file_transfer_client import FileTransferClient

# HTTP 클라이언트
client = FileTransferClient("http://localhost:5000")

# 파일 업로드
client.upload_file("test.txt")

# 파일 다운로드
client.download_file("test.txt", "downloaded_test.txt")

# 파일 목록
files = client.list_files()
print(files)
```

## 🔗 API 엔드포인트

### HTTP API
- `POST /upload` - 파일 업로드
- `GET /download/<filename>` - 파일 다운로드
- `GET /files` - 파일 목록 조회
- `GET /` - 웹 인터페이스

### 소켓 명령어
- `UPLOAD` - 파일 업로드
- `DOWNLOAD <filename>` - 파일 다운로드  
- `LIST` - 파일 목록 조회

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다.