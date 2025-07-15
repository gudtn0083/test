#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
음성 인식 시스템 설정 스크립트
"""

import os
import sys
import subprocess
import platform

def run_command(command, description=""):
    """명령어 실행 및 결과 확인"""
    print(f"\n{description}")
    print(f"실행 중: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ 성공")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 실패: {e}")
        if e.stderr:
            print(f"오류: {e.stderr}")
        return False

def install_system_dependencies():
    """시스템 의존성 패키지 설치"""
    print("=== 시스템 의존성 패키지 설치 ===")
    
    system = platform.system().lower()
    
    if system == "linux":
        # Ubuntu/Debian 기반
        if os.path.exists("/etc/debian_version"):
            commands = [
                "sudo apt-get update",
                "sudo apt-get install -y python3-pip",
                "sudo apt-get install -y ffmpeg",
                "sudo apt-get install -y portaudio19-dev python3-pyaudio",
                "sudo apt-get install -y flac",
                "sudo apt-get install -y libespeak-dev",
                "sudo apt-get install -y swig",
                "sudo apt-get install -y libpulse-dev"
            ]
        # CentOS/RHEL/Fedora 기반
        elif os.path.exists("/etc/redhat-release"):
            commands = [
                "sudo yum update -y",
                "sudo yum install -y python3-pip",
                "sudo yum install -y ffmpeg",
                "sudo yum install -y portaudio-devel",
                "sudo yum install -y flac",
                "sudo yum install -y espeak-devel",
                "sudo yum install -y swig",
                "sudo yum install -y pulseaudio-libs-devel"
            ]
        else:
            print("지원하지 않는 Linux 배포판입니다. 수동으로 의존성을 설치해주세요.")
            return False
        
        for cmd in commands:
            if not run_command(cmd, f"설치 중: {cmd.split()[-1]}"):
                print(f"경고: {cmd} 실행 실패")
                
    elif system == "darwin":  # macOS
        commands = [
            "brew install ffmpeg",
            "brew install portaudio",
            "brew install flac",
            "brew install swig"
        ]
        
        # Homebrew 설치 확인
        if not run_command("which brew", "Homebrew 확인"):
            print("Homebrew를 먼저 설치해주세요: https://brew.sh/")
            return False
        
        for cmd in commands:
            run_command(cmd, f"설치 중: {cmd.split()[-1]}")
            
    elif system == "windows":
        print("Windows에서는 다음 프로그램들을 수동으로 설치해주세요:")
        print("1. FFmpeg: https://ffmpeg.org/download.html")
        print("2. Microsoft Visual C++ Build Tools")
        print("3. Windows용 Python 개발 도구")
        
    return True

def install_python_dependencies():
    """Python 의존성 패키지 설치"""
    print("\n=== Python 의존성 패키지 설치 ===")
    
    # pip 업그레이드
    run_command("pip install --upgrade pip", "pip 업그레이드")
    
    # requirements.txt에서 패키지 설치
    if os.path.exists("requirements.txt"):
        run_command("pip install -r requirements.txt", "requirements.txt에서 패키지 설치")
    else:
        # 수동으로 필수 패키지 설치
        packages = [
            "SpeechRecognition==3.10.0",
            "pydub==0.25.1",
            "ffmpeg-python==0.2.0",
            "PyAudio==0.2.13",
            "pocketsphinx==0.1.15",
            "requests==2.31.0"
        ]
        
        for package in packages:
            run_command(f"pip install {package}", f"설치 중: {package}")

def test_installation():
    """설치 테스트"""
    print("\n=== 설치 테스트 ===")
    
    try:
        import speech_recognition as sr
        print("✓ SpeechRecognition 라이브러리 로드 성공")
        
        import pydub
        print("✓ pydub 라이브러리 로드 성공")
        
        # 마이크 테스트
        recognizer = sr.Recognizer()
        print("✓ 음성 인식기 초기화 성공")
        
        # 오디오 소스 확인
        try:
            with sr.Microphone() as source:
                print("✓ 마이크 접근 성공")
        except Exception as e:
            print(f"⚠ 마이크 접근 실패: {e}")
            print("  (마이크 없이도 파일 인식은 가능합니다)")
        
        print("\n설치가 성공적으로 완료되었습니다!")
        return True
        
    except Exception as e:
        print(f"✗ 설치 테스트 실패: {e}")
        return False

def create_sample_audio_directory():
    """샘플 오디오 파일 디렉토리 생성"""
    print("\n=== 샘플 디렉토리 생성 ===")
    
    audio_dir = "audio_files"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        print(f"✓ '{audio_dir}' 디렉토리 생성됨")
        
        # README 파일 생성
        with open(os.path.join(audio_dir, "README.txt"), "w", encoding="utf-8") as f:
            f.write("음성 파일 디렉토리\n")
            f.write("===================\n\n")
            f.write("이 디렉토리에 음성 파일을 넣고 일괄 처리할 수 있습니다.\n\n")
            f.write("지원하는 형식:\n")
            f.write("- WAV, MP3, MP4, M4A, FLAC, AAC, OGG, WMA\n\n")
            f.write("사용법:\n")
            f.write("python speech_recognition_system.py audio_files --batch\n")
        
        print("✓ README.txt 파일 생성됨")
    else:
        print(f"'{audio_dir}' 디렉토리가 이미 존재합니다.")

def main():
    print("=== 음성 인식 시스템 설정 ===")
    print("이 스크립트는 음성 인식 시스템을 설정합니다.")
    print(f"운영체제: {platform.system()} {platform.release()}")
    
    response = input("\n설정을 시작하시겠습니까? (y/n): ")
    if response.lower() != 'y':
        print("설정을 취소했습니다.")
        return
    
    # 1. 시스템 의존성 설치
    if input("\n시스템 의존성을 설치하시겠습니까? (y/n): ").lower() == 'y':
        install_system_dependencies()
    
    # 2. Python 의존성 설치
    if input("\nPython 의존성을 설치하시겠습니까? (y/n): ").lower() == 'y':
        install_python_dependencies()
    
    # 3. 설치 테스트
    if input("\n설치를 테스트하시겠습니까? (y/n): ").lower() == 'y':
        test_installation()
    
    # 4. 샘플 디렉토리 생성
    if input("\n샘플 디렉토리를 생성하시겠습니까? (y/n): ").lower() == 'y':
        create_sample_audio_directory()
    
    print("\n=== 설정 완료 ===")
    print("\n사용법:")
    print("1. 인터랙티브 모드: python speech_recognition_system.py")
    print("2. 파일 처리: python speech_recognition_system.py audio_file.wav")
    print("3. 일괄 처리: python speech_recognition_system.py audio_files --batch")
    print("4. 예제 실행: python example_usage.py")

if __name__ == "__main__":
    main()