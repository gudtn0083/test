# 다중 프로토콜 이메일 전송 시스템

SMTP, HTTP API, MQTT 세 가지 프로토콜을 사용하여 이메일을 전송하는 Python 애플리케이션입니다.

## 🚀 주요 기능

- **SMTP**: 전통적인 이메일 프로토콜을 통한 직접 전송
- **HTTP API**: SendGrid와 같은 RESTful API를 통한 전송
- **MQTT**: IoT 메시징 프로토콜을 통한 이메일 정보 발행/구독

## 📁 프로젝트 구조

```
.
├── mail_sender.py          # 기본 메일 발송 모듈
├── mail_sender_env.py      # 환경 변수를 사용하는 메일 발송 모듈
├── mqtt_subscriber.py      # MQTT 메시지 구독자
├── test_mail_sender.py     # 종합 테스트 스크립트
├── send_mqtt_test.py       # MQTT 테스트 스크립트
├── requirements.txt        # 필요한 패키지 목록
├── .env.example           # 환경 설정 예시
└── README.md              # 프로젝트 문서
```

## 🛠️ 설치 방법

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

또는 시스템 패키지로 설치:

```bash
pip install --break-system-packages -r requirements.txt
```

### 2. 환경 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 실제 값으로 수정합니다:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```env
# SMTP 설정 (Gmail 예시)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # Gmail의 경우 앱 비밀번호 사용

# HTTP API 설정 (SendGrid 예시)
SENDGRID_API_KEY=your_sendgrid_api_key

# MQTT 설정
MQTT_BROKER=broker.emqx.io  # 공개 브로커 사용 가능
MQTT_PORT=1883
MQTT_TOPIC=email/notifications

# 테스트 수신자 이메일
TEST_EMAIL=test@example.com
```

## 📧 사용 방법

### 기본 사용법

```python
from mail_sender_env import MultiProtocolMailSender

# 인스턴스 생성
sender = MultiProtocolMailSender()

# 이메일 정보
to_email = "recipient@example.com"
subject = "테스트 메일"
body = "안녕하세요, 테스트 메일입니다."

# SMTP로 전송
sender.send_via_smtp(to_email, subject, body)

# HTTP API로 전송
sender.send_via_http(to_email, subject, body)

# MQTT로 전송
sender.send_via_mqtt(to_email, subject, body)

# 모든 프로토콜로 동시 전송
sender.send_all_protocols(to_email, subject, body)
```

### 테스트 실행

1. **종합 테스트**:
   ```bash
   python3 test_mail_sender.py
   ```

2. **간단한 테스트**:
   ```bash
   python3 mail_sender.py
   ```

3. **MQTT 테스트**:
   ```bash
   # 터미널 1: 구독자 실행
   python3 mqtt_subscriber.py
   
   # 터미널 2: 메시지 발행
   python3 send_mqtt_test.py
   ```

## 🔧 프로토콜별 설정 가이드

### SMTP (Gmail 예시)

1. Gmail 계정에서 2단계 인증 활성화
2. [앱 비밀번호 생성](https://myaccount.google.com/apppasswords)
3. 생성된 앱 비밀번호를 `.env` 파일의 `SMTP_PASSWORD`에 설정

### HTTP API (SendGrid 예시)

1. [SendGrid](https://sendgrid.com) 계정 생성
2. API 키 생성
3. API 키를 `.env` 파일의 `SENDGRID_API_KEY`에 설정

### MQTT

- 기본적으로 공개 브로커 `broker.emqx.io` 사용
- 프라이빗 브로커 사용 시 `.env` 파일에서 설정 변경

## 📊 테스트 결과

현재 설정으로 테스트한 결과:

- **SMTP**: ❌ 인증 정보 필요
- **HTTP**: ❌ API 키 필요  
- **MQTT**: ✅ 즉시 사용 가능 (공개 브로커)

## 🔍 MQTT 메시지 형식

MQTT로 발행되는 메시지는 다음과 같은 JSON 형식입니다:

```json
{
  "timestamp": "2024-01-15T12:34:56.789012",
  "to": "recipient@example.com",
  "subject": "메일 제목",
  "body": "메일 본문",
  "from": "sender@example.com"
}
```

## ⚠️ 주의사항

1. **보안**: `.env` 파일은 절대 Git에 커밋하지 마세요
2. **MQTT**: 공개 브로커 사용 시 민감한 정보 전송 주의
3. **API 제한**: SendGrid 등의 서비스는 무료 계정에 전송 제한이 있습니다

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.