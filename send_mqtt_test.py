#!/usr/bin/env python3
"""MQTT 이메일 전송 테스트 스크립트"""

from mail_sender_env import MultiProtocolMailSender
from datetime import datetime

def main():
    # 메일 발송기 인스턴스 생성
    sender = MultiProtocolMailSender()
    
    # 테스트 이메일 정보
    test_email = "test@example.com"
    subject = f"MQTT 테스트 메일 - {datetime.now().strftime('%H:%M:%S')}"
    body = f"""
안녕하세요!

이 메일은 MQTT 프로토콜을 통해 전송된 테스트 메일입니다.

전송 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MQTT 브로커: {sender.mqtt_config['broker']}
토픽: {sender.mqtt_config['topic']}

이 메시지가 MQTT 구독자에게 표시되어야 합니다.

감사합니다.
"""
    
    print("📧 MQTT로 테스트 이메일을 전송합니다...")
    print(f"수신자: {test_email}")
    print(f"제목: {subject}")
    
    # MQTT로 전송
    result = sender.send_via_mqtt(test_email, subject, body)
    
    if result:
        print("\n✅ 전송 성공! MQTT 구독자 창을 확인하세요.")
    else:
        print("\n❌ 전송 실패!")

if __name__ == "__main__":
    main()