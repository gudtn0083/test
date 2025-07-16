# 📧 이메일 테스트 설정 가이드

이 가이드는 Python 이메일 테스트 스크립트를 사용하기 위한 설정 방법을 설명합니다.

## 🚀 빠른 시작

1. **간단한 테스트**: `python3 simple_email_test.py`
2. **종합 테스트**: `python3 email_test.py`

## 📋 주요 이메일 서비스 설정

### 1. Gmail 설정

#### 필요한 설정:
- **SMTP 서버**: `smtp.gmail.com`
- **포트**: `587`
- **보안**: TLS

#### 앱 비밀번호 생성 방법:
1. Google 계정 관리 → 보안
2. 2단계 인증 활성화 (필수)
3. "앱 비밀번호" 생성
4. 생성된 16자리 비밀번호 사용

```python
# Gmail 설정 예시
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-16-digit-app-password"
```

### 2. Outlook/Hotmail 설정

#### 필요한 설정:
- **SMTP 서버**: `smtp-mail.outlook.com`
- **포트**: `587`
- **보안**: TLS

```python
# Outlook 설정 예시
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@outlook.com"
SENDER_PASSWORD = "your-password"
```

### 3. Yahoo Mail 설정

#### 필요한 설정:
- **SMTP 서버**: `smtp.mail.yahoo.com`
- **포트**: `587`
- **보안**: TLS

#### 앱 비밀번호 생성:
1. Yahoo 계정 보안 → 앱 비밀번호
2. 새 앱 비밀번호 생성
3. 생성된 비밀번호 사용

### 4. Naver Mail 설정

#### 필요한 설정:
- **SMTP 서버**: `smtp.naver.com`
- **포트**: `587`
- **보안**: TLS

#### IMAP/SMTP 활성화:
1. 네이버 메일 → 환경설정
2. POP3/IMAP 설정 → IMAP/SMTP 사용
3. 외부메일 클라이언트 → 사용함

## 🔧 테스트 스크립트 사용법

### 종합 테스트 (`email_test.py`)

```bash
python3 email_test.py
```

**기능:**
- 다중 이메일 서비스 지원
- 텍스트 및 HTML 이메일 테스트
- 상세한 오류 진단
- 대화형 설정

### 간단한 테스트 (`simple_email_test.py`)

```bash
python3 simple_email_test.py
```

**기능:**
- 빠른 텍스트 이메일 테스트
- 기본 Gmail 설정
- 간단한 사용법

## 🛠️ 문제 해결

### 자주 발생하는 오류들

#### 1. 인증 실패 (SMTPAuthenticationError)
```
❌ 인증 실패: 이메일 주소나 비밀번호를 확인하세요.
```

**해결 방법:**
- Gmail: 앱 비밀번호 사용
- 2단계 인증 활성화 확인
- 올바른 이메일 주소 확인

#### 2. 연결 실패 (SMTPServerDisconnected)
```
❌ SMTP 서버 연결이 끊어졌습니다.
```

**해결 방법:**
- 네트워크 연결 확인
- 방화벽 설정 확인
- SMTP 서버 주소 및 포트 확인

#### 3. 수신자 거부 (SMTPRecipientsRefused)
```
❌ 수신자 주소가 거부되었습니다.
```

**해결 방법:**
- 수신자 이메일 주소 확인
- 스팸 필터 설정 확인

## 🔐 보안 권장사항

1. **환경변수 사용**:
   ```bash
   export EMAIL_PASSWORD="your-app-password"
   ```

2. **설정 파일 보안**:
   - `.gitignore`에 설정 파일 추가
   - 실제 비밀번호 노출 방지

3. **앱 비밀번호 사용**:
   - 기본 계정 비밀번호 대신 앱 전용 비밀번호 사용

## 📝 테스트 시나리오

### 기본 테스트
1. 텍스트 이메일 발송
2. 발송 시간 확인
3. 인코딩 테스트 (한글)

### 고급 테스트
1. HTML 이메일 발송
2. 첨부파일 포함 (선택사항)
3. 다중 수신자 테스트

## 🆘 지원

문제가 발생하면:
1. 오류 메시지 확인
2. 이메일 서비스 공식 문서 참조
3. 네트워크 및 방화벽 설정 확인

---

**💡 팁**: 처음 사용하시는 경우 `simple_email_test.py`로 시작하세요!