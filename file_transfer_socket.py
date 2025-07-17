import socket
import os
import threading
import struct
import time
from pathlib import Path

class SocketFileTransferServer:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.upload_folder = 'socket_uploads'
        
        # 업로드 폴더 생성
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def handle_client(self, conn, addr):
        """클라이언트 연결 처리"""
        print(f"📱 클라이언트 연결됨: {addr}")
        
        try:
            while True:
                # 명령어 수신
                command = conn.recv(1024).decode('utf-8')
                if not command:
                    break
                
                print(f"📩 명령어 수신: {command}")
                
                if command.startswith('UPLOAD'):
                    self.receive_file(conn)
                elif command.startswith('DOWNLOAD'):
                    filename = command.split(' ', 1)[1]
                    self.send_file(conn, filename)
                elif command == 'LIST':
                    self.send_file_list(conn)
                else:
                    conn.send(b'ERROR: Unknown command')
                    
        except Exception as e:
            print(f"❌ 클라이언트 처리 중 오류: {str(e)}")
        finally:
            conn.close()
            print(f"📱 클라이언트 연결 종료: {addr}")
    
    def receive_file(self, conn):
        """파일 수신"""
        try:
            # 파일 정보 수신 (파일명 길이 + 파일명 + 파일 크기)
            filename_length = struct.unpack('I', conn.recv(4))[0]
            filename = conn.recv(filename_length).decode('utf-8')
            file_size = struct.unpack('Q', conn.recv(8))[0]
            
            print(f"📥 파일 수신 시작: {filename} ({file_size} bytes)")
            
            # 중복 파일명 처리
            original_filename = filename
            counter = 1
            while os.path.exists(os.path.join(self.upload_folder, filename)):
                name, ext = os.path.splitext(original_filename)
                filename = f"{name}_{counter}{ext}"
                counter += 1
            
            filepath = os.path.join(self.upload_folder, filename)
            
            # 파일 수신
            received_size = 0
            with open(filepath, 'wb') as file:
                while received_size < file_size:
                    chunk_size = min(4096, file_size - received_size)
                    chunk = conn.recv(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    received_size += len(chunk)
                    
                    # 진행률 표시
                    progress = (received_size / file_size) * 100
                    print(f"\r📥 진행률: {progress:.1f}%", end='', flush=True)
            
            print(f"\n✅ 파일 수신 완료: {filename}")
            conn.send(b'SUCCESS')
            
        except Exception as e:
            print(f"\n❌ 파일 수신 실패: {str(e)}")
            conn.send(b'ERROR')
    
    def send_file(self, conn, filename):
        """파일 송신"""
        try:
            filepath = os.path.join(self.upload_folder, filename)
            
            if not os.path.exists(filepath):
                conn.send(b'ERROR: File not found')
                return
            
            file_size = os.path.getsize(filepath)
            print(f"📤 파일 송신 시작: {filename} ({file_size} bytes)")
            
            # 파일 정보 송신
            conn.send(struct.pack('Q', file_size))
            
            # 파일 송신
            sent_size = 0
            with open(filepath, 'rb') as file:
                while sent_size < file_size:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    conn.send(chunk)
                    sent_size += len(chunk)
                    
                    # 진행률 표시
                    progress = (sent_size / file_size) * 100
                    print(f"\r📤 진행률: {progress:.1f}%", end='', flush=True)
            
            print(f"\n✅ 파일 송신 완료: {filename}")
            
        except Exception as e:
            print(f"\n❌ 파일 송신 실패: {str(e)}")
            conn.send(b'ERROR')
    
    def send_file_list(self, conn):
        """파일 목록 송신"""
        try:
            files = []
            for filename in os.listdir(self.upload_folder):
                filepath = os.path.join(self.upload_folder, filename)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    files.append(f"{filename}:{size}")
            
            file_list = '\n'.join(files)
            conn.send(file_list.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ 파일 목록 송신 실패: {str(e)}")
            conn.send(b'ERROR')
    
    def start(self):
        """서버 시작"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"🚀 소켓 파일 전송 서버 시작: {self.host}:{self.port}")
            print(f"📁 업로드 폴더: {self.upload_folder}")
            
            while True:
                conn, addr = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n⏹️ 서버를 종료합니다.")
        except Exception as e:
            print(f"❌ 서버 오류: {str(e)}")
        finally:
            server_socket.close()

class SocketFileTransferClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
    
    def connect(self):
        """서버에 연결"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"✅ 서버에 연결됨: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ 서버 연결 실패: {str(e)}")
            return False
    
    def upload_file(self, file_path):
        """파일 업로드"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
                return False
            
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            print(f"📤 파일 업로드 시작: {filename} ({file_size} bytes)")
            
            # 업로드 명령어 송신
            self.socket.send(b'UPLOAD')
            
            # 파일 정보 송신
            filename_bytes = filename.encode('utf-8')
            self.socket.send(struct.pack('I', len(filename_bytes)))
            self.socket.send(filename_bytes)
            self.socket.send(struct.pack('Q', file_size))
            
            # 파일 송신
            sent_size = 0
            with open(file_path, 'rb') as file:
                while sent_size < file_size:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    self.socket.send(chunk)
                    sent_size += len(chunk)
                    
                    # 진행률 표시
                    progress = (sent_size / file_size) * 100
                    print(f"\r📤 진행률: {progress:.1f}%", end='', flush=True)
            
            # 응답 수신
            response = self.socket.recv(1024).decode('utf-8')
            if response == 'SUCCESS':
                print(f"\n✅ 업로드 성공: {filename}")
                return True
            else:
                print(f"\n❌ 업로드 실패: {response}")
                return False
                
        except Exception as e:
            print(f"\n❌ 업로드 중 오류: {str(e)}")
            return False
    
    def download_file(self, filename, save_path=None):
        """파일 다운로드"""
        try:
            if save_path is None:
                save_path = f"downloaded_{filename}"
            
            print(f"📥 파일 다운로드 시작: {filename}")
            
            # 다운로드 명령어 송신
            command = f"DOWNLOAD {filename}"
            self.socket.send(command.encode('utf-8'))
            
            # 응답 확인
            response = self.socket.recv(1024)
            if response.startswith(b'ERROR'):
                print(f"❌ 다운로드 실패: {response.decode('utf-8')}")
                return False
            
            # 파일 크기 수신
            file_size = struct.unpack('Q', response)[0]
            
            # 파일 수신
            received_size = 0
            with open(save_path, 'wb') as file:
                while received_size < file_size:
                    chunk_size = min(4096, file_size - received_size)
                    chunk = self.socket.recv(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    received_size += len(chunk)
                    
                    # 진행률 표시
                    progress = (received_size / file_size) * 100
                    print(f"\r📥 진행률: {progress:.1f}%", end='', flush=True)
            
            print(f"\n✅ 다운로드 성공: {save_path}")
            return True
            
        except Exception as e:
            print(f"\n❌ 다운로드 중 오류: {str(e)}")
            return False
    
    def list_files(self):
        """파일 목록 조회"""
        try:
            self.socket.send(b'LIST')
            response = self.socket.recv(4096).decode('utf-8')
            
            if response == 'ERROR':
                print("❌ 파일 목록 조회 실패")
                return []
            
            if not response.strip():
                print("📁 서버에 파일이 없습니다.")
                return []
            
            files = []
            print("📁 서버의 파일 목록:")
            for i, line in enumerate(response.strip().split('\n'), 1):
                filename, size = line.split(':')
                size_mb = round(int(size) / (1024 * 1024), 2)
                size_str = f'{size_mb} MB' if size_mb > 1 else f'{round(int(size) / 1024, 2)} KB'
                print(f"  {i}. {filename} ({size_str})")
                files.append(filename)
            
            return files
            
        except Exception as e:
            print(f"❌ 파일 목록 조회 중 오류: {str(e)}")
            return []
    
    def close(self):
        """연결 종료"""
        if hasattr(self, 'socket'):
            self.socket.close()

def run_server():
    """서버 실행"""
    server = SocketFileTransferServer()
    server.start()

def run_client():
    """클라이언트 실행"""
    client = SocketFileTransferClient()
    
    if not client.connect():
        return
    
    try:
        while True:
            print("\n" + "="*50)
            print("🚀 소켓 파일 전송 클라이언트")
            print("="*50)
            print("1. 파일 업로드")
            print("2. 파일 다운로드")
            print("3. 서버 파일 목록 보기")
            print("4. 종료")
            print("-"*50)
            
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
                            filename = files[index]
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
    finally:
        client.close()

def main():
    print("🚀 소켓 기반 파일 전송 프로그램")
    print("1. 서버 실행")
    print("2. 클라이언트 실행")
    
    choice = input("선택하세요 (1-2): ").strip()
    
    if choice == '1':
        run_server()
    elif choice == '2':
        run_client()
    else:
        print("❌ 잘못된 선택입니다.")

if __name__ == "__main__":
    main()