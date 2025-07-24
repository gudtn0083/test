import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class EmailMQTTSubscriber:
    """MQTT를 통해 이메일 정보를 구독하는 클래스"""
    
    def __init__(self):
        self.broker = os.getenv('MQTT_BROKER', 'broker.emqx.io')
        self.port = int(os.getenv('MQTT_PORT', '1883'))
        self.topic = os.getenv('MQTT_TOPIC', 'email/notifications')
        self.client = mqtt.Client()
        
        # 콜백 함수 설정
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    
    def on_connect(self, client, userdata, flags, rc):
        """브로커 연결 시 호출되는 콜백"""
        if rc == 0:
            print(f"✅ MQTT 브로커에 연결되었습니다: {self.broker}:{self.port}")
            print(f"📡 토픽 구독 중: {self.topic}")
            client.subscribe(self.topic)
        else:
            print(f"❌ 연결 실패. 오류 코드: {rc}")
    
    def on_message(self, client, userdata, msg):
        """메시지 수신 시 호출되는 콜백"""
        try:
            # 메시지 디코딩
            payload = msg.payload.decode('utf-8')
            email_data = json.loads(payload)
            
            # 수신 시간
            received_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print("\n" + "="*60)
            print("📧 새로운 이메일 메시지 수신!")
            print("="*60)
            print(f"수신 시간: {received_time}")
            print(f"토픽: {msg.topic}")
            print("-"*60)
            print(f"발신자: {email_data.get('from', 'N/A')}")
            print(f"수신자: {email_data.get('to', 'N/A')}")
            print(f"제목: {email_data.get('subject', 'N/A')}")
            print(f"전송 시간: {email_data.get('timestamp', 'N/A')}")
            print("-"*60)
            print("본문:")
            print(email_data.get('body', 'N/A'))
            print("="*60 + "\n")
            
            # 로그 파일에 저장 (선택사항)
            self.save_to_log(email_data, received_time)
            
        except json.JSONDecodeError:
            print(f"❌ JSON 디코딩 오류: {payload}")
        except Exception as e:
            print(f"❌ 메시지 처리 오류: {str(e)}")
    
    def on_disconnect(self, client, userdata, rc):
        """연결 해제 시 호출되는 콜백"""
        if rc != 0:
            print(f"⚠️  예상치 못한 연결 해제. 오류 코드: {rc}")
    
    def save_to_log(self, email_data, received_time):
        """수신된 이메일 정보를 로그 파일에 저장"""
        try:
            log_entry = {
                'received_time': received_time,
                'email_data': email_data
            }
            
            with open('mqtt_email_log.json', 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n')
                
        except Exception as e:
            print(f"⚠️  로그 저장 실패: {str(e)}")
    
    def start(self):
        """구독자 시작"""
        print(f"\n🚀 MQTT 이메일 구독자 시작")
        print(f"브로커: {self.broker}:{self.port}")
        print(f"토픽: {self.topic}")
        print("메시지 대기 중... (종료하려면 Ctrl+C를 누르세요)\n")
        
        try:
            # 브로커에 연결
            self.client.connect(self.broker, self.port, 60)
            
            # 메시지 루프 시작 (블로킹)
            self.client.loop_forever()
            
        except KeyboardInterrupt:
            print("\n\n👋 구독자를 종료합니다...")
            self.client.disconnect()
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    subscriber = EmailMQTTSubscriber()
    subscriber.start()