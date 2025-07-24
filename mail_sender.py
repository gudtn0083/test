import smtplib
import requests
import paho.mqtt.client as mqtt
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class MultiProtocolMailSender:
    """다중 프로토콜을 사용하여 이메일을 전송하는 클래스"""
    
    def __init__(self):
        self.smtp_config = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': 'your_email@gmail.com',
            'password': 'your_app_password'
        }
        
        self.http_config = {
            'url': 'https://api.sendgrid.com/v3/mail/send',
            'api_key': 'your_sendgrid_api_key'
        }
        
        self.mqtt_config = {
            'broker': 'broker.emqx.io',
            'port': 1883,
            'topic': 'email/notifications'
        }
    
    def send_via_smtp(self, to_email, subject, body):
        """SMTP를 통해 이메일 전송"""
        try:
            # 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # 본문 추가
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # SMTP 서버 연결
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            
            # 이메일 전송
            text = msg.as_string()
            server.sendmail(self.smtp_config['username'], to_email, text)
            server.quit()
            
            print(f"✅ SMTP: 이메일이 성공적으로 전송되었습니다 - {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ SMTP 오류: {str(e)}")
            return False
    
    def send_via_http(self, to_email, subject, body):
        """HTTP API (SendGrid)를 통해 이메일 전송"""
        try:
            headers = {
                'Authorization': f'Bearer {self.http_config["api_key"]}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'personalizations': [{
                    'to': [{'email': to_email}]
                }],
                'from': {'email': self.smtp_config['username']},
                'subject': subject,
                'content': [{
                    'type': 'text/plain',
                    'value': body
                }]
            }
            
            response = requests.post(
                self.http_config['url'],
                headers=headers,
                json=data
            )
            
            if response.status_code == 202:
                print(f"✅ HTTP: 이메일이 성공적으로 전송되었습니다 - {to_email}")
                return True
            else:
                print(f"❌ HTTP 오류: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ HTTP 오류: {str(e)}")
            return False
    
    def send_via_mqtt(self, to_email, subject, body):
        """MQTT를 통해 이메일 정보 발행"""
        try:
            # MQTT 클라이언트 생성
            client = mqtt.Client()
            
            # 연결 콜백 설정
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    print("✅ MQTT: 브로커에 연결되었습니다")
                else:
                    print(f"❌ MQTT 연결 실패: {rc}")
            
            def on_publish(client, userdata, mid):
                print(f"✅ MQTT: 메시지가 성공적으로 발행되었습니다 - Message ID: {mid}")
            
            client.on_connect = on_connect
            client.on_publish = on_publish
            
            # 브로커에 연결
            client.connect(self.mqtt_config['broker'], self.mqtt_config['port'], 60)
            client.loop_start()
            
            # 이메일 데이터 준비
            email_data = {
                'timestamp': datetime.now().isoformat(),
                'to': to_email,
                'subject': subject,
                'body': body,
                'from': self.smtp_config['username']
            }
            
            # 메시지 발행
            result = client.publish(
                self.mqtt_config['topic'],
                json.dumps(email_data, ensure_ascii=False),
                qos=1
            )
            
            # 발행 완료 대기
            result.wait_for_publish()
            
            client.loop_stop()
            client.disconnect()
            
            return True
            
        except Exception as e:
            print(f"❌ MQTT 오류: {str(e)}")
            return False
    
    def send_all_protocols(self, to_email, subject, body):
        """모든 프로토콜을 사용하여 이메일 전송"""
        print("\n" + "="*50)
        print("📧 다중 프로토콜 이메일 전송 시작")
        print("="*50 + "\n")
        
        results = {
            'SMTP': self.send_via_smtp(to_email, subject, body),
            'HTTP': self.send_via_http(to_email, subject, body),
            'MQTT': self.send_via_mqtt(to_email, subject, body)
        }
        
        print("\n" + "="*50)
        print("📊 전송 결과 요약")
        print("="*50)
        for protocol, success in results.items():
            status = "✅ 성공" if success else "❌ 실패"
            print(f"{protocol}: {status}")
        
        return results


# 테스트용 이메일 내용
def create_test_email():
    """테스트용 이메일 내용 생성"""
    subject = "다중 프로토콜 이메일 테스트"
    body = f"""
안녕하세요,

이 메일은 다중 프로토콜(SMTP, HTTP, MQTT)을 통해 전송된 테스트 메일입니다.

전송 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

각 프로토콜별 특징:
- SMTP: 전통적인 이메일 프로토콜
- HTTP: RESTful API를 통한 이메일 전송
- MQTT: IoT 메시징 프로토콜을 통한 이메일 정보 발행

감사합니다.
"""
    return subject, body


if __name__ == "__main__":
    # 메일 발송기 인스턴스 생성
    sender = MultiProtocolMailSender()
    
    # 테스트 이메일 정보
    test_email = "test@example.com"
    subject, body = create_test_email()
    
    print("🚀 이메일 전송 테스트를 시작합니다...\n")
    
    # 개별 프로토콜 테스트
    print("1️⃣ SMTP 프로토콜 테스트")
    sender.send_via_smtp(test_email, subject + " (SMTP)", body)
    time.sleep(1)
    
    print("\n2️⃣ HTTP 프로토콜 테스트")
    sender.send_via_http(test_email, subject + " (HTTP)", body)
    time.sleep(1)
    
    print("\n3️⃣ MQTT 프로토콜 테스트")
    sender.send_via_mqtt(test_email, subject + " (MQTT)", body)
    time.sleep(1)
    
    # 모든 프로토콜 동시 테스트
    print("\n4️⃣ 모든 프로토콜 동시 테스트")
    sender.send_all_protocols(test_email, subject + " (ALL)", body)