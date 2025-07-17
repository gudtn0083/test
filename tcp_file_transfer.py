#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import struct
import threading
import hashlib
import time
from pathlib import Path

class TCPFileTransferServer:
    """TCP 프로토콜 기반 파일 전송 서버"""
    
    def __init__(self, host='0.0.0.0', port=8888, upload_dir='tcp_uploads'):
        self.host = host
        self.port = port
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.running = False
        
    def start_server(self):
        """TCP 서버 시작"""
        # TCP 소켓 생성 (SOCK_STREAM = TCP)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)  # 최대 10개 연결 대기
            self.running = True
            
            print(f"🚀 TCP 파일 전송 서버 시작")
            print(f"📡 주소: {self.host}:{self.port}")
            print(f"📁 업로드 폴더: {self.upload_dir}")
            print(f"🔗 프로토콜: TCP (SOCK_STREAM)")
            print("-" * 50)
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"📱 새 연결: {client_address}")
                    
                    # 각 클라이언트를 별도 스레드에서 처리
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"❌ 서버 오류: {e}")
                        
        except Exception as e:
            print(f"❌ 서버 시작 실패: {e}")
        finally:
            self.server_socket.close()
            
    def handle_client(self, client_socket, client_address):
        """클라이언트 연결 처리"""
        try:
            while True:
                # 명령어 수신 (4바이트 길이 + 명령어)
                try:
                    cmd_length_data = self.recv_exact(client_socket, 4)
                    if not cmd_length_data:
                        break
                        
                    cmd_length = struct.unpack('!I', cmd_length_data)[0]
                    command = client_socket.recv(cmd_length).decode('utf-8')
                    
                    print(f"📩 {client_address}: {command}")
                    
                    if command.startswith('UPLOAD'):
                        self.handle_upload(client_socket, client_address)
                    elif command.startswith('DOWNLOAD'):
                        filename = command.split(' ', 1)[1] if ' ' in command else ''
                        self.handle_download(client_socket, client_address, filename)
                    elif command == 'LIST':
                        self.handle_list(client_socket, client_address)
                    elif command == 'QUIT':
                        break
                    else:
                        self.send_response(client_socket, 'ERROR', 'Unknown command')
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"❌ 명령 처리 오류: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ 클라이언트 처리 오류: {e}")
        finally:
            client_socket.close()
            print(f"📱 연결 종료: {client_address}")
            
    def handle_upload(self, client_socket, client_address):
        """파일 업로드 처리"""
        try:
            # 파일 정보 수신
            info_data = self.recv_exact(client_socket, 12)  # filename_len(4) + filesize(8)
            filename_len, file_size = struct.unpack('!IQ', info_data)
            
            filename = client_socket.recv(filename_len).decode('utf-8')
            
            # 안전한 파일명으로 변경
            safe_filename = self.sanitize_filename(filename)
            file_path = self.upload_dir / safe_filename
            
            # 중복 파일명 처리
            counter = 1
            original_path = file_path
            while file_path.exists():
                name_part = original_path.stem
                ext_part = original_path.suffix
                file_path = self.upload_dir / f"{name_part}_{counter}{ext_part}"
                counter += 1
            
            print(f"📥 {client_address}: 업로드 시작 - {safe_filename} ({file_size:,} bytes)")
            
            # 파일 수신
            received = 0
            hash_md5 = hashlib.md5()
            
            with open(file_path, 'wb') as f:
                while received < file_size:
                    chunk_size = min(8192, file_size - received)
                    chunk = client_socket.recv(chunk_size)
                    if not chunk:
                        raise Exception("연결이 끊어졌습니다")
                    
                    f.write(chunk)
                    hash_md5.update(chunk)
                    received += len(chunk)
                    
                    # 진행률 출력 (10% 단위)
                    progress = (received / file_size) * 100
                    if received == file_size or int(progress) % 10 == 0:
                        print(f"\r📥 {client_address}: {progress:.1f}% ({received:,}/{file_size:,})", end='')
            
            print(f"\n✅ {client_address}: 업로드 완료 - {safe_filename}")
            print(f"🔑 MD5: {hash_md5.hexdigest()}")
            
            # 성공 응답
            self.send_response(client_socket, 'SUCCESS', f'File uploaded: {safe_filename}')
            
        except Exception as e:
            print(f"\n❌ {client_address}: 업로드 실패 - {e}")
            self.send_response(client_socket, 'ERROR', str(e))
            
    def handle_download(self, client_socket, client_address, filename):
        """파일 다운로드 처리"""
        try:
            file_path = self.upload_dir / filename
            
            if not file_path.exists() or not file_path.is_file():
                self.send_response(client_socket, 'ERROR', 'File not found')
                return
                
            file_size = file_path.stat().st_size
            print(f"📤 {client_address}: 다운로드 시작 - {filename} ({file_size:,} bytes)")
            
            # 파일 정보 송신
            self.send_response(client_socket, 'SUCCESS', f'{file_size}')
            
            # 파일 송신
            sent = 0
            with open(file_path, 'rb') as f:
                while sent < file_size:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    client_socket.sendall(chunk)
                    sent += len(chunk)
                    
                    # 진행률 출력
                    progress = (sent / file_size) * 100
                    print(f"\r📤 {client_address}: {progress:.1f}% ({sent:,}/{file_size:,})", end='')
            
            print(f"\n✅ {client_address}: 다운로드 완료 - {filename}")
            
        except Exception as e:
            print(f"\n❌ {client_address}: 다운로드 실패 - {e}")
            self.send_response(client_socket, 'ERROR', str(e))
            
    def handle_list(self, client_socket, client_address):
        """파일 목록 처리"""
        try:
            files = []
            for file_path in self.upload_dir.iterdir():
                if file_path.is_file():
                    size = file_path.stat().st_size
                    modified = file_path.stat().st_mtime
                    files.append(f"{file_path.name}|{size}|{modified}")
            
            file_list = '\n'.join(files)
            self.send_response(client_socket, 'SUCCESS', file_list)
            print(f"📋 {client_address}: 파일 목록 전송 ({len(files)}개)")
            
        except Exception as e:
            print(f"❌ {client_address}: 파일 목록 실패 - {e}")
            self.send_response(client_socket, 'ERROR', str(e))
            
    def recv_exact(self, sock, size):
        """정확한 크기만큼 데이터 수신"""
        data = b''
        while len(data) < size:
            chunk = sock.recv(size - len(data))
            if not chunk:
                return None
            data += chunk
        return data
        
    def send_response(self, client_socket, status, message):
        """응답 메시지 송신"""
        response = f"{status}|{message}"
        response_bytes = response.encode('utf-8')
        
        # 응답 길이 + 응답 데이터 송신
        client_socket.send(struct.pack('!I', len(response_bytes)))
        client_socket.send(response_bytes)
        
    def sanitize_filename(self, filename):
        """안전한 파일명으로 변환"""
        # 위험한 문자 제거
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # 경로 순회 방지
        filename = os.path.basename(filename)
        
        return filename[:255]  # 파일명 길이 제한
        
    def stop_server(self):
        """서버 중지"""
        self.running = False
        if hasattr(self, 'server_socket'):
            self.server_socket.close()

class TCPFileTransferClient:
    """TCP 프로토콜 기반 파일 전송 클라이언트"""
    
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """서버에 연결"""
        try:
            # TCP 소켓 생성
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"✅ TCP 서버에 연결됨: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ 연결 실패: {e}")
            return False
            
    def send_command(self, command):
        """명령어 송신"""
        cmd_bytes = command.encode('utf-8')
        self.socket.send(struct.pack('!I', len(cmd_bytes)))
        self.socket.send(cmd_bytes)
        
    def recv_response(self):
        """응답 수신"""
        response_len_data = self.recv_exact(4)
        if not response_len_data:
            return None, None
            
        response_len = struct.unpack('!I', response_len_data)[0]
        response = self.socket.recv(response_len).decode('utf-8')
        
        parts = response.split('|', 1)
        status = parts[0]
        message = parts[1] if len(parts) > 1 else ''
        
        return status, message
        
    def upload_file(self, file_path):
        """파일 업로드"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
                return False
                
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            print(f"📤 업로드 시작: {filename} ({file_size:,} bytes)")
            
            # 업로드 명령 송신
            self.send_command('UPLOAD')
            
            # 파일 정보 송신
            filename_bytes = filename.encode('utf-8')
            file_info = struct.pack('!IQ', len(filename_bytes), file_size)
            self.socket.send(file_info)
            self.socket.send(filename_bytes)
            
            # 파일 데이터 송신
            sent = 0
            hash_md5 = hashlib.md5()
            
            with open(file_path, 'rb') as f:
                while sent < file_size:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    self.socket.sendall(chunk)
                    hash_md5.update(chunk)
                    sent += len(chunk)
                    
                    progress = (sent / file_size) * 100
                    print(f"\r📤 진행률: {progress:.1f}% ({sent:,}/{file_size:,})", end='')
            
            print(f"\n🔑 MD5: {hash_md5.hexdigest()}")
            
            # 응답 수신
            status, message = self.recv_response()
            if status == 'SUCCESS':
                print(f"✅ 업로드 성공: {message}")
                return True
            else:
                print(f"❌ 업로드 실패: {message}")
                return False
                
        except Exception as e:
            print(f"❌ 업로드 오류: {e}")
            return False
            
    def download_file(self, filename, save_path=None):
        """파일 다운로드"""
        try:
            if save_path is None:
                save_path = f"tcp_downloaded_{filename}"
                
            print(f"📥 다운로드 시작: {filename}")
            
            # 다운로드 명령 송신
            self.send_command(f'DOWNLOAD {filename}')
            
            # 응답 수신
            status, message = self.recv_response()
            if status != 'SUCCESS':
                print(f"❌ 다운로드 실패: {message}")
                return False
                
            file_size = int(message)
            print(f"📁 파일 크기: {file_size:,} bytes")
            
            # 파일 데이터 수신
            received = 0
            hash_md5 = hashlib.md5()
            
            with open(save_path, 'wb') as f:
                while received < file_size:
                    chunk_size = min(8192, file_size - received)
                    chunk = self.socket.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    hash_md5.update(chunk)
                    received += len(chunk)
                    
                    progress = (received / file_size) * 100
                    print(f"\r📥 진행률: {progress:.1f}% ({received:,}/{file_size:,})", end='')
            
            print(f"\n🔑 MD5: {hash_md5.hexdigest()}")
            print(f"✅ 다운로드 성공: {save_path}")
            return True
            
        except Exception as e:
            print(f"❌ 다운로드 오류: {e}")
            return False
            
    def list_files(self):
        """파일 목록 조회"""
        try:
            self.send_command('LIST')
            status, message = self.recv_response()
            
            if status != 'SUCCESS':
                print(f"❌ 목록 조회 실패: {message}")
                return []
                
            if not message.strip():
                print("📁 서버에 파일이 없습니다.")
                return []
                
            files = []
            print("📁 서버 파일 목록:")
            print("-" * 60)
            
            for i, line in enumerate(message.strip().split('\n'), 1):
                parts = line.split('|')
                filename = parts[0]
                size = int(parts[1])
                modified = float(parts[2])
                
                size_str = self.format_size(size)
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modified))
                
                print(f"{i:2d}. {filename:<30} {size_str:>10} {time_str}")
                files.append(filename)
                
            print("-" * 60)
            return files
            
        except Exception as e:
            print(f"❌ 목록 조회 오류: {e}")
            return []
            
    def recv_exact(self, size):
        """정확한 크기만큼 데이터 수신"""
        data = b''
        while len(data) < size:
            chunk = self.socket.recv(size - len(data))
            if not chunk:
                return None
            data += chunk
        return data
        
    def format_size(self, size):
        """파일 크기 포맷팅"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
        
    def close(self):
        """연결 종료"""
        if self.socket:
            try:
                self.send_command('QUIT')
            except:
                pass
            self.socket.close()

def run_server():
    """서버 실행"""
    server = TCPFileTransferServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n⏹️ 서버를 종료합니다.")
        server.stop_server()

def run_client():
    """클라이언트 실행"""
    client = TCPFileTransferClient()
    
    if not client.connect():
        return
        
    try:
        while True:
            print("\n" + "=" * 60)
            print("🚀 TCP 파일 전송 클라이언트")
            print("=" * 60)
            print("1. 파일 업로드")
            print("2. 파일 다운로드") 
            print("3. 파일 목록 보기")
            print("4. 종료")
            print("-" * 60)
            
            choice = input("선택하세요 (1-4): ").strip()
            
            if choice == '1':
                file_path = input("업로드할 파일 경로: ").strip()
                if file_path:
                    client.upload_file(file_path)
                    
            elif choice == '2':
                files = client.list_files()
                if files:
                    try:
                        idx = int(input("다운로드할 파일 번호: ")) - 1
                        if 0 <= idx < len(files):
                            filename = files[idx]
                            save_path = input(f"저장할 경로 (기본: tcp_downloaded_{filename}): ").strip()
                            if not save_path:
                                save_path = f"tcp_downloaded_{filename}"
                            client.download_file(filename, save_path)
                        else:
                            print("❌ 잘못된 번호입니다.")
                    except ValueError:
                        print("❌ 숫자를 입력하세요.")
                        
            elif choice == '3':
                client.list_files()
                
            elif choice == '4':
                print("👋 종료합니다.")
                break
                
            else:
                print("❌ 1-4 사이의 숫자를 입력하세요.")
                
    except KeyboardInterrupt:
        print("\n👋 클라이언트를 종료합니다.")
    finally:
        client.close()

def main():
    print("🚀 TCP 프로토콜 파일 전송 시스템")
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