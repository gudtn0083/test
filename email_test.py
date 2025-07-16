#!/usr/bin/env python3
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import getpass

class EmailTester:
    def __init__(self):
        self.smtp_servers = {
            'gmail': {'server': 'smtp.gmail.com', 'port': 587},
            'outlook': {'server': 'smtp-mail.outlook.com', 'port': 587},
            'yahoo': {'server': 'smtp.mail.yahoo.com', 'port': 587},
            'naver': {'server': 'smtp.naver.com', 'port': 587},
            'custom': {'server': '', 'port': 587}
        }
    
    def get_email_config(self):
        """이메일 설정 입력받기"""
        print("=== 이메일 테스트 설정 ===")
        print("지원되는 이메일 서비스:")
        for key, value in self.smtp_servers.items():
            if key != 'custom':
                print(f"  {key}: {value['server']}")
        print("  custom: 직접 입력")
        
        provider = input("\n이메일 서비스를 선택하세요 (gmail/outlook/yahoo/naver/custom): ").lower()
        
        if provider not in self.smtp_servers:
            print("지원되지 않는 서비스입니다. Gmail로 설정합니다.")
            provider = 'gmail'
        
        if provider == 'custom':
            smtp_server = input("SMTP 서버 주소를 입력하세요: ")
            smtp_port = int(input("SMTP 포트를 입력하세요 (기본값 587): ") or "587")
            self.smtp_servers['custom'] = {'server': smtp_server, 'port': smtp_port}
        
        sender_email = input("발신자 이메일 주소: ")
        sender_password = getpass.getpass("발신자 이메일 비밀번호 (또는 앱 비밀번호): ")
        recipient_email = input("수신자 이메일 주소: ")
        
        return {
            'provider': provider,
            'sender_email': sender_email,
            'sender_password': sender_password,
            'recipient_email': recipient_email,
            'smtp_server': self.smtp_servers[provider]['server'],
            'smtp_port': self.smtp_servers[provider]['port']
        }
    
    def create_test_email(self, sender_email, recipient_email, test_type="basic"):
        """테스트 이메일 생성"""
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if test_type == "basic":
            message["Subject"] = f"이메일 테스트 - {current_time}"
            body = f"""
이메일 발송 테스트입니다.

발송 시간: {current_time}
발신자: {sender_email}
수신자: {recipient_email}

이 메일을 받으셨다면 이메일 설정이 정상적으로 작동하고 있습니다!

테스트 완료 ✅
            """
        
        elif test_type == "html":
            message["Subject"] = f"HTML 이메일 테스트 - {current_time}"
            body = f"""
            <html>
                <body>
                    <h2>🚀 이메일 테스트</h2>
                    <p><strong>발송 시간:</strong> {current_time}</p>
                    <p><strong>발신자:</strong> {sender_email}</p>
                    <p><strong>수신자:</strong> {recipient_email}</p>
                    
                    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px;">
                        <h3>✅ 테스트 성공!</h3>
                        <p>이 HTML 이메일을 정상적으로 받으셨다면 이메일 설정이 완벽하게 작동하고 있습니다.</p>
                    </div>
                    
                    <hr>
                    <p><em>Python 이메일 테스트 스크립트로 발송됨</em></p>
                </body>
            </html>
            """
            message.attach(MIMEText(body, "html"))
            return message
        
        message.attach(MIMEText(body, "plain"))
        return message
    
    def send_email(self, config, test_type="basic"):
        """이메일 발송"""
        try:
            print(f"\n📧 {test_type} 이메일 발송 중...")
            
            # 이메일 메시지 생성
            message = self.create_test_email(
                config['sender_email'], 
                config['recipient_email'], 
                test_type
            )
            
            # SMTP 서버 연결
            context = ssl.create_default_context()
            
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(config['sender_email'], config['sender_password'])
                
                text = message.as_string()
                server.sendmail(config['sender_email'], config['recipient_email'], text)
            
            print(f"✅ {test_type} 이메일이 성공적으로 발송되었습니다!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ 인증 실패: 이메일 주소나 비밀번호를 확인하세요.")
            print("   Gmail의 경우 '앱 비밀번호'를 사용해야 할 수 있습니다.")
            return False
            
        except smtplib.SMTPRecipientsRefused:
            print("❌ 수신자 주소가 거부되었습니다.")
            return False
            
        except smtplib.SMTPServerDisconnected:
            print("❌ SMTP 서버 연결이 끊어졌습니다.")
            return False
            
        except Exception as e:
            print(f"❌ 이메일 발송 실패: {str(e)}")
            return False
    
    def run_comprehensive_test(self):
        """종합 이메일 테스트 실행"""
        print("🔍 이메일 발송 종합 테스트를 시작합니다.\n")
        
        config = self.get_email_config()
        
        print(f"\n📋 설정 정보:")
        print(f"   SMTP 서버: {config['smtp_server']}:{config['smtp_port']}")
        print(f"   발신자: {config['sender_email']}")
        print(f"   수신자: {config['recipient_email']}")
        
        input("\n테스트를 시작하려면 Enter 키를 누르세요...")
        
        # 기본 텍스트 이메일 테스트
        success1 = self.send_email(config, "basic")
        
        if success1:
            # HTML 이메일 테스트
            if input("\nHTML 이메일도 테스트하시겠습니까? (y/n): ").lower() == 'y':
                success2 = self.send_email(config, "html")
        
        print("\n" + "="*50)
        print("📊 테스트 결과 요약:")
        print(f"   기본 텍스트 이메일: {'✅ 성공' if success1 else '❌ 실패'}")
        if 'success2' in locals():
            print(f"   HTML 이메일: {'✅ 성공' if success2 else '❌ 실패'}")
        print("="*50)

def create_email_config_file():
    """이메일 설정 파일 생성"""
    config_template = """# 이메일 테스트 설정 파일
# 보안을 위해 실제 사용시에는 환경변수를 사용하세요.

# Gmail 설정 예시
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"  # Gmail 앱 비밀번호
RECIPIENT_EMAIL = "recipient@example.com"

# 다른 이메일 서비스 설정
# Outlook: smtp-mail.outlook.com:587
# Yahoo: smtp.mail.yahoo.com:587
# Naver: smtp.naver.com:587
"""
    
    with open('email_config_template.txt', 'w', encoding='utf-8') as f:
        f.write(config_template)
    
    print("📄 이메일 설정 템플릿 파일이 생성되었습니다: email_config_template.txt")

def main():
    print("📮 이메일 테스트 프로그램")
    print("=" * 30)
    
    choice = input("""
선택하세요:
1. 대화형 이메일 테스트 실행
2. 설정 파일 템플릿 생성
3. 종료

선택 (1-3): """)
    
    if choice == "1":
        tester = EmailTester()
        tester.run_comprehensive_test()
    elif choice == "2":
        create_email_config_file()
    elif choice == "3":
        print("프로그램을 종료합니다.")
    else:
        print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()