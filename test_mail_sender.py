#!/usr/bin/env python3
"""
다중 프로토콜 이메일 전송 테스트 스크립트
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from mail_sender_env import MultiProtocolMailSender, create_test_email


def print_header(title):
    """헤더 출력"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60 + "\n")


def check_dependencies():
    """필요한 패키지 확인 및 설치"""
    print_header("의존성 패키지 확인")
    
    required_packages = ['requests', 'paho-mqtt', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 설치됨")
        except ImportError:
            print(f"❌ {package} 미설치")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n설치가 필요한 패키지: {', '.join(missing_packages)}")
        install = input("패키지를 설치하시겠습니까? (y/n): ")
        if install.lower() == 'y':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ 패키지 설치 완료")
        else:
            print("⚠️  패키지 설치를 건너뜁니다. 일부 기능이 작동하지 않을 수 있습니다.")
    
    return len(missing_packages) == 0


def check_environment():
    """환경 설정 확인"""
    print_header("환경 설정 확인")
    
    if not os.path.exists('.env'):
        print("⚠️  .env 파일이 없습니다.")
        create_env = input(".env.example을 복사하여 .env를 생성하시겠습니까? (y/n): ")
        if create_env.lower() == 'y':
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env 파일이 생성되었습니다.")
            print("⚠️  .env 파일을 열어 실제 값으로 수정해주세요.")
            return False
    else:
        print("✅ .env 파일이 존재합니다.")
    
    return True


def test_smtp_connection(sender):
    """SMTP 연결 테스트"""
    print_header("SMTP 연결 테스트")
    
    try:
        import smtplib
        server = smtplib.SMTP(sender.smtp_config['server'], sender.smtp_config['port'])
        server.starttls()
        server.quit()
        print("✅ SMTP 서버 연결 성공")
        return True
    except Exception as e:
        print(f"❌ SMTP 서버 연결 실패: {str(e)}")
        return False


def test_mqtt_connection(sender):
    """MQTT 브로커 연결 테스트"""
    print_header("MQTT 브로커 연결 테스트")
    
    try:
        import paho.mqtt.client as mqtt
        
        connected = False
        
        def on_connect(client, userdata, flags, rc):
            nonlocal connected
            if rc == 0:
                connected = True
                client.disconnect()
        
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(sender.mqtt_config['broker'], sender.mqtt_config['port'], 60)
        client.loop_start()
        
        # 연결 대기 (최대 5초)
        for _ in range(50):
            if connected:
                break
            time.sleep(0.1)
        
        client.loop_stop()
        
        if connected:
            print("✅ MQTT 브로커 연결 성공")
            return True
        else:
            print("❌ MQTT 브로커 연결 실패")
            return False
            
    except Exception as e:
        print(f"❌ MQTT 브로커 연결 오류: {str(e)}")
        return False


def run_mqtt_subscriber():
    """MQTT 구독자를 백그라운드에서 실행"""
    print("📡 MQTT 구독자를 백그라운드에서 실행합니다...")
    
    # 새 터미널에서 구독자 실행
    if sys.platform == "win32":
        subprocess.Popen(['start', 'cmd', '/k', 'python', 'mqtt_subscriber.py'], shell=True)
    else:
        subprocess.Popen(['gnome-terminal', '--', 'python3', 'mqtt_subscriber.py'])
    
    time.sleep(2)  # 구독자가 시작될 때까지 대기


def main():
    """메인 테스트 함수"""
    print("\n" + "🚀 " * 20)
    print("다중 프로토콜 이메일 전송 시스템 테스트")
    print("🚀 " * 20 + "\n")
    
    # 1. 의존성 확인
    if not check_dependencies():
        print("\n⚠️  의존성 패키지가 설치되지 않았습니다.")
        return
    
    # 2. 환경 설정 확인
    if not check_environment():
        print("\n⚠️  환경 설정을 완료한 후 다시 실행해주세요.")
        return
    
    # 3. 메일 발송기 인스턴스 생성
    sender = MultiProtocolMailSender()
    
    # 4. 연결 테스트
    smtp_ok = test_smtp_connection(sender)
    mqtt_ok = test_mqtt_connection(sender)
    
    # 5. MQTT 구독자 실행 여부 확인
    if mqtt_ok:
        run_subscriber = input("\nMQTT 구독자를 실행하시겠습니까? (y/n): ")
        if run_subscriber.lower() == 'y':
            run_mqtt_subscriber()
    
    # 6. 테스트 이메일 전송
    print_header("이메일 전송 테스트")
    
    test_email = input("테스트 이메일 주소를 입력하세요 (기본값: test@example.com): ").strip()
    if not test_email:
        test_email = "test@example.com"
    
    subject, body = create_test_email()
    
    # 프로토콜 선택
    print("\n전송할 프로토콜을 선택하세요:")
    print("1. SMTP만")
    print("2. HTTP만")
    print("3. MQTT만")
    print("4. 모든 프로토콜")
    print("5. 개별 테스트 (각각 실행)")
    
    choice = input("\n선택 (1-5): ").strip()
    
    if choice == '1':
        sender.send_via_smtp(test_email, subject + " (SMTP)", body)
    elif choice == '2':
        sender.send_via_http(test_email, subject + " (HTTP)", body)
    elif choice == '3':
        sender.send_via_mqtt(test_email, subject + " (MQTT)", body)
    elif choice == '4':
        sender.send_all_protocols(test_email, subject + " (ALL)", body)
    elif choice == '5':
        print("\n개별 프로토콜 테스트를 시작합니다...")
        
        if smtp_ok:
            print("\n1️⃣ SMTP 테스트")
            sender.send_via_smtp(test_email, subject + " (SMTP)", body)
            time.sleep(1)
        
        print("\n2️⃣ HTTP 테스트")
        sender.send_via_http(test_email, subject + " (HTTP)", body)
        time.sleep(1)
        
        if mqtt_ok:
            print("\n3️⃣ MQTT 테스트")
            sender.send_via_mqtt(test_email, subject + " (MQTT)", body)
            time.sleep(1)
    else:
        print("잘못된 선택입니다.")
    
    # 7. 결과 요약
    print_header("테스트 완료")
    print("테스트가 완료되었습니다.")
    print("\n참고사항:")
    print("- SMTP: 실제 이메일 전송을 위해서는 올바른 인증 정보가 필요합니다.")
    print("- HTTP: SendGrid API 키가 필요합니다.")
    print("- MQTT: 공개 브로커를 사용하므로 즉시 테스트 가능합니다.")
    
    if os.path.exists('mqtt_email_log.json'):
        print("\n📄 MQTT 로그 파일: mqtt_email_log.json")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 테스트를 중단합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")