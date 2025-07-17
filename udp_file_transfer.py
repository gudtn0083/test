#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import struct
import threading
import hashlib
import time
import json
from pathlib import Path
from collections import defaultdict
import random

class UDPPacket:
    """UDP 패킷 클래스"""
    
    # 패킷 타입 정의
    TYPE_COMMAND = 1
    TYPE_DATA = 2
    TYPE_ACK = 3
    TYPE_NACK = 4
    TYPE_FIN = 5
    
    def __init__(self, packet_type, seq_num, data=b'', checksum=0):
        self.packet_type = packet_type
        self.seq_num = seq_num
        self.data = data
        self.checksum = checksum or self._calculate_checksum(data)
        
    def _calculate_checksum(self, data):
        """간단한 체크섬 계산"""
        return sum(data) % 65536
        
    def pack(self):
        """패킷을 바이트로 직렬화"""
        header = struct.pack('!HHH', self.packet_type, self.seq_num, self.checksum)
        return header + self.data
        
    @classmethod
    def unpack(cls, data):
        """바이트에서 패킷 역직렬화"""
        if len(data) < 6:
            return None
        header = data[:6]
        packet_data = data[6:]
        packet_type, seq_num, checksum = struct.unpack('!HHH', header)
        return cls(packet_type, seq_num, packet_data, checksum)
        
    def is_valid(self):
        """패킷 무결성 검증"""
        return self.checksum == self._calculate_checksum(self.data)

class UDPFileTransferServer:
    """UDP 프로토콜 기반 파일 전송 서버"""
    
    def __init__(self, host='0.0.0.0', port=7777, upload_dir='udp_uploads'):
        self.host = host
        self.port = port
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.socket = None
        self.running = False
        self.clients = {}  # 클라이언트별 상태 관리
        self.max_packet_size = 1400  # MTU 고려
        
    def start_server(self):
        """UDP 서버 시작"""
        # UDP 소켓 생성 (SOCK_DGRAM = UDP)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind((self.host, self.port))
            self.running = True
            
            print(f"🚀 UDP 파일 전송 서버 시작")
            print(f"📡 주소: {self.host}:{self.port}")
            print(f"📁 업로드 폴더: {self.upload_dir}")
            print(f"🔗 프로토콜: UDP (SOCK_DGRAM)")
            print(f"📦 최대 패킷 크기: {self.max_packet_size} bytes")
            print("-" * 50)
            
            while self.running:
                try:
                    data, client_address = self.socket.recvfrom(self.max_packet_size + 100)
                    packet = UDPPacket.unpack(data)
                    
                    if packet and packet.is_valid():
                        threading.Thread(
                            target=self.handle_packet,
                            args=(packet, client_address),
                            daemon=True
                        ).start()
                    else:
                        print(f"❌ 잘못된 패킷 수신: {client_address}")
                        
                except socket.error as e:
                    if self.running:
                        print(f"❌ 소켓 오류: {e}")
                        
        except Exception as e:
            print(f"❌ 서버 시작 실패: {e}")
        finally:
            if self.socket:
                self.socket.close()
                
    def handle_packet(self, packet, client_address):
        """패킷 처리"""
        client_key = f"{client_address[0]}:{client_address[1]}"
        
        if packet.packet_type == UDPPacket.TYPE_COMMAND:
            self.handle_command(packet, client_address, client_key)
        elif packet.packet_type == UDPPacket.TYPE_DATA:
            self.handle_data_packet(packet, client_address, client_key)
        elif packet.packet_type == UDPPacket.TYPE_ACK:
            self.handle_ack(packet, client_address, client_key)
            
    def handle_command(self, packet, client_address, client_key):
        """명령어 처리"""
        try:
            command_data = json.loads(packet.data.decode('utf-8'))
            command = command_data.get('command', '')
            
            print(f"📩 {client_address}: {command}")
            
            if command == 'UPLOAD':
                self.init_upload_session(command_data, client_address, client_key)
            elif command == 'DOWNLOAD':
                self.init_download_session(command_data, client_address, client_key)
            elif command == 'LIST':
                self.send_file_list(client_address)
                
        except Exception as e:
            print(f"❌ 명령 처리 오류: {e}")
            
    def init_upload_session(self, command_data, client_address, client_key):
        """업로드 세션 초기화"""
        filename = command_data.get('filename', '')
        file_size = command_data.get('file_size', 0)
        total_packets = command_data.get('total_packets', 0)
        
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
        
        # 클라이언트 세션 초기화
        self.clients[client_key] = {
            'mode': 'upload',
            'file_path': file_path,
            'file_size': file_size,
            'total_packets': total_packets,
            'received_packets': {},
            'expected_seq': 0,
            'last_activity': time.time()
        }
        
        print(f"📥 {client_address}: 업로드 세션 시작 - {safe_filename} ({file_size:,} bytes, {total_packets} 패킷)")
        
        # ACK 응답
        ack_data = json.dumps({'status': 'ready', 'filename': safe_filename}).encode('utf-8')
        ack_packet = UDPPacket(UDPPacket.TYPE_ACK, 0, ack_data)
        self.socket.sendto(ack_packet.pack(), client_address)
        
    def handle_data_packet(self, packet, client_address, client_key):
        """데이터 패킷 처리"""
        if client_key not in self.clients:
            return
            
        client_session = self.clients[client_key]
        client_session['last_activity'] = time.time()
        
        seq_num = packet.seq_num
        client_session['received_packets'][seq_num] = packet.data
        
        # 진행률 출력
        received_count = len(client_session['received_packets'])
        total_packets = client_session['total_packets']
        progress = (received_count / total_packets) * 100
        
        if received_count % 50 == 0 or received_count == total_packets:
            print(f"\r📥 {client_address}: {progress:.1f}% ({received_count}/{total_packets})", end='')
        
        # ACK 전송
        ack_packet = UDPPacket(UDPPacket.TYPE_ACK, seq_num)
        self.socket.sendto(ack_packet.pack(), client_address)
        
        # 모든 패킷 수신 완료 확인
        if received_count == total_packets:
            self.finalize_upload(client_address, client_key)
            
    def finalize_upload(self, client_address, client_key):
        """업로드 완료 처리"""
        client_session = self.clients[client_key]
        
        try:
            # 순서대로 파일 재구성
            with open(client_session['file_path'], 'wb') as f:
                for seq_num in sorted(client_session['received_packets'].keys()):
                    f.write(client_session['received_packets'][seq_num])
            
            # 파일 크기 검증
            actual_size = client_session['file_path'].stat().st_size
            expected_size = client_session['file_size']
            
            if actual_size == expected_size:
                print(f"\n✅ {client_address}: 업로드 완료 - {client_session['file_path'].name}")
                
                # 완료 확인 전송
                fin_data = json.dumps({'status': 'complete', 'message': 'Upload successful'}).encode('utf-8')
                fin_packet = UDPPacket(UDPPacket.TYPE_FIN, 0, fin_data)
                self.socket.sendto(fin_packet.pack(), client_address)
            else:
                print(f"\n❌ {client_address}: 파일 크기 불일치 ({actual_size} != {expected_size})")
                
        except Exception as e:
            print(f"\n❌ {client_address}: 업로드 완료 처리 실패 - {e}")
        finally:
            del self.clients[client_key]
            
    def init_download_session(self, command_data, client_address, client_key):
        """다운로드 세션 초기화"""
        filename = command_data.get('filename', '')
        file_path = self.upload_dir / filename
        
        if not file_path.exists():
            error_data = json.dumps({'status': 'error', 'message': 'File not found'}).encode('utf-8')
            nack_packet = UDPPacket(UDPPacket.TYPE_NACK, 0, error_data)
            self.socket.sendto(nack_packet.pack(), client_address)
            return
            
        file_size = file_path.stat().st_size
        data_per_packet = self.max_packet_size - 50  # 헤더 여유분
        total_packets = (file_size + data_per_packet - 1) // data_per_packet
        
        print(f"📤 {client_address}: 다운로드 시작 - {filename} ({file_size:,} bytes, {total_packets} 패킷)")
        
        # 클라이언트 세션 초기화
        self.clients[client_key] = {
            'mode': 'download',
            'file_path': file_path,
            'file_size': file_size,
            'total_packets': total_packets,
            'sent_packets': set(),
            'acked_packets': set(),
            'current_seq': 0,
            'last_activity': time.time()
        }
        
        # 파일 정보 응답
        info_data = json.dumps({
            'status': 'ready',
            'file_size': file_size,
            'total_packets': total_packets,
            'data_per_packet': data_per_packet
        }).encode('utf-8')
        ack_packet = UDPPacket(UDPPacket.TYPE_ACK, 0, info_data)
        self.socket.sendto(ack_packet.pack(), client_address)
        
        # 데이터 전송 시작
        threading.Thread(
            target=self.send_file_data,
            args=(client_address, client_key),
            daemon=True
        ).start()
        
    def send_file_data(self, client_address, client_key):
        """파일 데이터 전송"""
        if client_key not in self.clients:
            return
            
        client_session = self.clients[client_key]
        file_path = client_session['file_path']
        data_per_packet = self.max_packet_size - 50
        
        try:
            with open(file_path, 'rb') as f:
                seq_num = 0
                while seq_num < client_session['total_packets']:
                    # 윈도우 기반 전송 (동시에 최대 10개 패킷)
                    window_size = 10
                    window_start = seq_num
                    
                    # 윈도우 내 패킷들 전송
                    for i in range(window_size):
                        if seq_num >= client_session['total_packets']:
                            break
                            
                        if seq_num not in client_session['sent_packets']:
                            f.seek(seq_num * data_per_packet)
                            data = f.read(data_per_packet)
                            
                            if data:
                                data_packet = UDPPacket(UDPPacket.TYPE_DATA, seq_num, data)
                                self.socket.sendto(data_packet.pack(), client_address)
                                client_session['sent_packets'].add(seq_num)
                                
                        seq_num += 1
                    
                    # ACK 대기 (타임아웃 포함)
                    time.sleep(0.1)
                    
                    # ACK된 패킷들 확인하여 윈도우 이동
                    while (window_start in client_session['acked_packets'] and 
                           window_start < client_session['total_packets']):
                        window_start += 1
                    
                    seq_num = window_start
                    
                    # 진행률 출력
                    acked_count = len(client_session['acked_packets'])
                    progress = (acked_count / client_session['total_packets']) * 100
                    if acked_count % 50 == 0:
                        print(f"\r📤 {client_address}: {progress:.1f}% ({acked_count}/{client_session['total_packets']})", end='')
                    
                    # 완료 확인
                    if acked_count == client_session['total_packets']:
                        break
                        
            print(f"\n✅ {client_address}: 다운로드 완료 - {file_path.name}")
            
        except Exception as e:
            print(f"\n❌ {client_address}: 다운로드 실패 - {e}")
        finally:
            if client_key in self.clients:
                del self.clients[client_key]
                
    def handle_ack(self, packet, client_address, client_key):
        """ACK 패킷 처리"""
        if client_key in self.clients:
            client_session = self.clients[client_key]
            if client_session.get('mode') == 'download':
                client_session['acked_packets'].add(packet.seq_num)
                client_session['last_activity'] = time.time()
                
    def send_file_list(self, client_address):
        """파일 목록 전송"""
        try:
            files = []
            for file_path in self.upload_dir.iterdir():
                if file_path.is_file():
                    size = file_path.stat().st_size
                    modified = file_path.stat().st_mtime
                    files.append({
                        'name': file_path.name,
                        'size': size,
                        'modified': modified
                    })
            
            response_data = json.dumps({'status': 'success', 'files': files}).encode('utf-8')
            
            # 큰 데이터는 여러 패킷으로 분할
            max_data_size = self.max_packet_size - 50
            for i in range(0, len(response_data), max_data_size):
                chunk = response_data[i:i + max_data_size]
                packet = UDPPacket(UDPPacket.TYPE_ACK, i // max_data_size, chunk)
                self.socket.sendto(packet.pack(), client_address)
                time.sleep(0.01)  # 패킷 간격
            
            # 전송 완료 신호
            fin_packet = UDPPacket(UDPPacket.TYPE_FIN, 0, b'list_complete')
            self.socket.sendto(fin_packet.pack(), client_address)
            
            print(f"📋 {client_address}: 파일 목록 전송 ({len(files)}개)")
            
        except Exception as e:
            print(f"❌ {client_address}: 파일 목록 실패 - {e}")
            
    def sanitize_filename(self, filename):
        """안전한 파일명으로 변환"""
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        filename = os.path.basename(filename)
        return filename[:255]
        
    def stop_server(self):
        """서버 중지"""
        self.running = False
        if self.socket:
            self.socket.close()

class UDPFileTransferClient:
    """UDP 프로토콜 기반 파일 전송 클라이언트"""
    
    def __init__(self, host='localhost', port=7777):
        self.host = host
        self.port = port
        self.socket = None
        self.max_packet_size = 1400
        self.timeout = 5.0
        
    def connect(self):
        """소켓 초기화 (UDP는 연결이 없으므로 소켓만 생성)"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)
            print(f"✅ UDP 소켓 생성: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ 소켓 생성 실패: {e}")
            return False
            
    def send_command(self, command_data):
        """명령어 전송"""
        data = json.dumps(command_data).encode('utf-8')
        packet = UDPPacket(UDPPacket.TYPE_COMMAND, 0, data)
        self.socket.sendto(packet.pack(), (self.host, self.port))
        
    def upload_file(self, file_path):
        """파일 업로드"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
                return False
                
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            data_per_packet = self.max_packet_size - 50
            total_packets = (file_size + data_per_packet - 1) // data_per_packet
            
            print(f"📤 업로드 시작: {filename} ({file_size:,} bytes, {total_packets} 패킷)")
            
            # 업로드 명령 전송
            command_data = {
                'command': 'UPLOAD',
                'filename': filename,
                'file_size': file_size,
                'total_packets': total_packets
            }
            self.send_command(command_data)
            
            # ACK 대기
            data, server_address = self.socket.recvfrom(self.max_packet_size)
            ack_packet = UDPPacket.unpack(data)
            
            if not ack_packet or ack_packet.packet_type != UDPPacket.TYPE_ACK:
                print("❌ 서버 응답 오류")
                return False
                
            response = json.loads(ack_packet.data.decode('utf-8'))
            if response.get('status') != 'ready':
                print(f"❌ 서버 준비 실패: {response.get('message', '')}")
                return False
                
            print(f"✅ 서버 준비 완료: {response.get('filename', filename)}")
            
            # 파일 데이터 전송
            sent_packets = 0
            hash_md5 = hashlib.md5()
            
            with open(file_path, 'rb') as f:
                seq_num = 0
                while seq_num < total_packets:
                    data_chunk = f.read(data_per_packet)
                    if not data_chunk:
                        break
                        
                    hash_md5.update(data_chunk)
                    
                    # 데이터 패킷 전송
                    data_packet = UDPPacket(UDPPacket.TYPE_DATA, seq_num, data_chunk)
                    self.socket.sendto(data_packet.pack(), (self.host, self.port))
                    
                    # ACK 대기
                    try:
                        ack_data, _ = self.socket.recvfrom(self.max_packet_size)
                        ack_packet = UDPPacket.unpack(ack_data)
                        
                        if ack_packet and ack_packet.packet_type == UDPPacket.TYPE_ACK:
                            sent_packets += 1
                            seq_num += 1
                            
                            # 진행률 출력
                            progress = (sent_packets / total_packets) * 100
                            print(f"\r📤 진행률: {progress:.1f}% ({sent_packets}/{total_packets})", end='')
                        else:
                            # 재전송
                            f.seek(seq_num * data_per_packet)
                            
                    except socket.timeout:
                        # 타임아웃 시 재전송
                        f.seek(seq_num * data_per_packet)
            
            # 완료 확인 대기
            try:
                fin_data, _ = self.socket.recvfrom(self.max_packet_size)
                fin_packet = UDPPacket.unpack(fin_data)
                
                if fin_packet and fin_packet.packet_type == UDPPacket.TYPE_FIN:
                    response = json.loads(fin_packet.data.decode('utf-8'))
                    if response.get('status') == 'complete':
                        print(f"\n🔑 MD5: {hash_md5.hexdigest()}")
                        print(f"✅ 업로드 성공: {response.get('message', '')}")
                        return True
                        
            except socket.timeout:
                pass
                
            print(f"\n⚠️ 업로드 완료 확인 못함 (타임아웃)")
            return True
            
        except Exception as e:
            print(f"❌ 업로드 오류: {e}")
            return False
            
    def download_file(self, filename, save_path=None):
        """파일 다운로드"""
        try:
            if save_path is None:
                save_path = f"udp_downloaded_{filename}"
                
            print(f"📥 다운로드 시작: {filename}")
            
            # 다운로드 명령 전송
            command_data = {
                'command': 'DOWNLOAD',
                'filename': filename
            }
            self.send_command(command_data)
            
            # 응답 대기
            data, server_address = self.socket.recvfrom(self.max_packet_size)
            response_packet = UDPPacket.unpack(data)
            
            if not response_packet:
                print("❌ 서버 응답 없음")
                return False
                
            if response_packet.packet_type == UDPPacket.TYPE_NACK:
                error = json.loads(response_packet.data.decode('utf-8'))
                print(f"❌ 다운로드 실패: {error.get('message', '')}")
                return False
                
            # 파일 정보 파싱
            file_info = json.loads(response_packet.data.decode('utf-8'))
            file_size = file_info.get('file_size', 0)
            total_packets = file_info.get('total_packets', 0)
            
            print(f"📁 파일 크기: {file_size:,} bytes ({total_packets} 패킷)")
            
            # 데이터 수신
            received_packets = {}
            hash_md5 = hashlib.md5()
            
            while len(received_packets) < total_packets:
                try:
                    data, _ = self.socket.recvfrom(self.max_packet_size + 100)
                    packet = UDPPacket.unpack(data)
                    
                    if packet and packet.packet_type == UDPPacket.TYPE_DATA and packet.is_valid():
                        if packet.seq_num not in received_packets:
                            received_packets[packet.seq_num] = packet.data
                            
                            # 진행률 출력
                            progress = (len(received_packets) / total_packets) * 100
                            print(f"\r📥 진행률: {progress:.1f}% ({len(received_packets)}/{total_packets})", end='')
                        
                        # ACK 전송
                        ack_packet = UDPPacket(UDPPacket.TYPE_ACK, packet.seq_num)
                        self.socket.sendto(ack_packet.pack(), (self.host, self.port))
                        
                except socket.timeout:
                    continue
                    
            # 파일 재구성
            with open(save_path, 'wb') as f:
                for seq_num in sorted(received_packets.keys()):
                    data_chunk = received_packets[seq_num]
                    f.write(data_chunk)
                    hash_md5.update(data_chunk)
            
            print(f"\n🔑 MD5: {hash_md5.hexdigest()}")
            print(f"✅ 다운로드 성공: {save_path}")
            return True
            
        except Exception as e:
            print(f"❌ 다운로드 오류: {e}")
            return False
            
    def list_files(self):
        """파일 목록 조회"""
        try:
            command_data = {'command': 'LIST'}
            self.send_command(command_data)
            
            # 응답 수신 (여러 패킷으로 올 수 있음)
            response_data = b''
            while True:
                try:
                    data, _ = self.socket.recvfrom(self.max_packet_size)
                    packet = UDPPacket.unpack(data)
                    
                    if packet:
                        if packet.packet_type == UDPPacket.TYPE_ACK:
                            response_data += packet.data
                        elif packet.packet_type == UDPPacket.TYPE_FIN:
                            break
                            
                except socket.timeout:
                    break
                    
            if not response_data:
                print("📁 서버에 파일이 없습니다.")
                return []
                
            response = json.loads(response_data.decode('utf-8'))
            files = response.get('files', [])
            
            if not files:
                print("📁 서버에 파일이 없습니다.")
                return []
                
            print("📁 서버 파일 목록:")
            print("-" * 60)
            
            file_names = []
            for i, file_info in enumerate(files, 1):
                filename = file_info['name']
                size = file_info['size']
                modified = file_info['modified']
                
                size_str = self.format_size(size)
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modified))
                
                print(f"{i:2d}. {filename:<30} {size_str:>10} {time_str}")
                file_names.append(filename)
                
            print("-" * 60)
            return file_names
            
        except Exception as e:
            print(f"❌ 목록 조회 오류: {e}")
            return []
            
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
            self.socket.close()

def run_server():
    """서버 실행"""
    server = UDPFileTransferServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n⏹️ 서버를 종료합니다.")
        server.stop_server()

def run_client():
    """클라이언트 실행"""
    client = UDPFileTransferClient()
    
    if not client.connect():
        return
        
    try:
        while True:
            print("\n" + "=" * 60)
            print("🚀 UDP 파일 전송 클라이언트")
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
                            save_path = input(f"저장할 경로 (기본: udp_downloaded_{filename}): ").strip()
                            if not save_path:
                                save_path = f"udp_downloaded_{filename}"
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
    print("🚀 UDP 프로토콜 파일 전송 시스템")
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