#!/usr/bin/env python3
"""
간단한 이메일 테스트 스크립트
빠른 테스트를 위한 간소화된 버전
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime

def send_test_email():
    """간단한 테스트 이메일 발송"""
    
    # 설정 (실제 사용시 수정 필요)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # 사용자 입력
    sender_email = input("발신자 이메일: ")
    sender_password = input("비밀번호 (앱 비밀번호): ")
    recipient_email = input("수신자 이메일: ")
    
    # 이메일 메시지 생성
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"테스트 메일 - {current_time}"
    body = f"""
안녕하세요!

이것은 Python에서 발송된 테스트 이메일입니다.

발송 시간: {current_time}
발신자: {sender_email}
수신자: {recipient_email}

테스트 성공! ✅
    """
    
    message = MIMEText(body, "plain", "utf-8")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    
    try:
        print("\n📧 이메일 발송 중...")
        
        # SMTP 연결 및 발송
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print("✅ 이메일이 성공적으로 발송되었습니다!")
        
    except Exception as e:
        print(f"❌ 이메일 발송 실패: {str(e)}")
        print("\n💡 문제 해결 팁:")
        print("   - Gmail의 경우 '앱 비밀번호'를 사용하세요")
        print("   - 2단계 인증이 활성화되어 있는지 확인하세요")
        print("   - '보안 수준이 낮은 앱의 액세스' 설정을 확인하세요")

if __name__ == "__main__":
    print("📮 간단한 이메일 테스트")
    print("=" * 25)
    send_test_email()