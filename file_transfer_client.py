import requests
import os
from pathlib import Path

class FileTransferClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        
    def upload_file(self, file_path):
        """파일을 서버에 업로드"""
        try:
            if not os.path.exists(file_path):
                print(f"파일을 찾을 수 없습니다: {file_path}")
                return False
            
            filename = os.path.basename(file_path)
            print(f"파일 업로드 중: {filename}")
            
            with open(file_path, 'rb') as file:
                files = {'file': (filename, file)}
                response = requests.post(f"{self.server_url}/upload", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 업로드 성공: {result['message']}")
                return True
            else:
                error = response.json().get('error', '알 수 없는 오류')
                print(f"❌ 업로드 실패: {error}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
            return False
        except Exception as e:
            print(f"❌ 업로드 중 오류 발생: {str(e)}")
            return False
    
    def download_file(self, filename, save_path=None):
        """서버에서 파일을 다운로드"""
        try:
            if save_path is None:
                save_path = f"downloaded_{filename}"
            
            print(f"파일 다운로드 중: {filename}")
            
            response = requests.get(f"{self.server_url}/download/{filename}")
            
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"✅ 다운로드 성공: {save_path}")
                return True
            else:
                print(f"❌ 다운로드 실패: 파일을 찾을 수 없습니다.")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
            return False
        except Exception as e:
            print(f"❌ 다운로드 중 오류 발생: {str(e)}")
            return False
    
    def list_files(self):
        """서버의 파일 목록을 가져옴"""
        try:
            response = requests.get(f"{self.server_url}/files")
            
            if response.status_code == 200:
                files = response.json()
                if files:
                    print("📁 서버의 파일 목록:")
                    for i, file in enumerate(files, 1):
                        print(f"  {i}. {file['name']} ({file['size']})")
                    return files
                else:
                    print("📁 서버에 파일이 없습니다.")
                    return []
            else:
                print("❌ 파일 목록을 가져올 수 없습니다.")
                return []
                
        except requests.exceptions.ConnectionError:
            print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
            return []
        except Exception as e:
            print(f"❌ 파일 목록 조회 중 오류 발생: {str(e)}")
            return []

def main():
    client = FileTransferClient()
    
    while True:
        print("\n" + "="*50)
        print("🚀 파일 전송 클라이언트")
        print("="*50)
        print("1. 파일 업로드")
        print("2. 파일 다운로드")
        print("3. 서버 파일 목록 보기")
        print("4. 종료")
        print("-"*50)
        
        try:
            choice = input("선택하세요 (1-4): ").strip()
            
            if choice == '1':
                file_path = input("업로드할 파일 경로를 입력하세요: ").strip()
                if file_path:
                    client.upload_file(file_path)
                    
            elif choice == '2':
                files = client.list_files()
                if files:
                    try:
                        index = int(input("다운로드할 파일 번호를 입력하세요: ")) - 1
                        if 0 <= index < len(files):
                            filename = files[index]['name']
                            save_path = input(f"저장할 경로를 입력하세요 (기본값: downloaded_{filename}): ").strip()
                            if not save_path:
                                save_path = f"downloaded_{filename}"
                            client.download_file(filename, save_path)
                        else:
                            print("❌ 잘못된 파일 번호입니다.")
                    except ValueError:
                        print("❌ 숫자를 입력해주세요.")
                        
            elif choice == '3':
                client.list_files()
                
            elif choice == '4':
                print("👋 프로그램을 종료합니다.")
                break
                
            else:
                print("❌ 잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요.")
                
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()