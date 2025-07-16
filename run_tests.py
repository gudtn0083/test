#!/usr/bin/env python3
"""
이미지 이진화 모듈 테스트 실행 스크립트
"""

import sys
import os
import subprocess

def run_basic_tests():
    """기본 테스트 실행"""
    print("🧪 기본 테스트 실행 중...")
    try:
        result = subprocess.run([
            sys.executable, "test_binary_converters.py", "--quick"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("에러:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"테스트 실행 중 오류 발생: {e}")
        return False

def run_full_tests():
    """전체 테스트 실행"""
    print("🔬 전체 테스트 실행 중...")
    try:
        result = subprocess.run([
            sys.executable, "test_binary_converters.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("에러:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"테스트 실행 중 오류 발생: {e}")
        return False

def check_dependencies():
    """필요한 패키지들이 설치되어 있는지 확인"""
    required_packages = ['cv2', 'numpy', 'matplotlib', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'numpy':
                import numpy
            elif package == 'matplotlib':
                import matplotlib
            elif package == 'PIL':
                from PIL import Image
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 누락된 패키지: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        print("pip install opencv-python numpy matplotlib pillow")
        return False
    else:
        print("✅ 모든 필요한 패키지가 설치되어 있습니다.")
        return True

def main():
    """메인 함수"""
    print("=== 이미지 이진화 모듈 테스트 ===\n")
    
    # 의존성 확인
    if not check_dependencies():
        return 1
    
    # 테스트 파일 존재 확인
    if not os.path.exists("test_binary_converters.py"):
        print("❌ 테스트 파일을 찾을 수 없습니다: test_binary_converters.py")
        return 1
    
    # 테스트할 모듈 파일들 확인
    required_files = ["simple_binary_converter.py", "binary_image_converter.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ 필요한 파일들이 누락되었습니다: {', '.join(missing_files)}")
        return 1
    
    print("✅ 모든 필요한 파일이 있습니다.\n")
    
    # 사용자 선택
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        print("테스트 유형을 선택하세요:")
        print("1. 기본 테스트 (빠른 실행)")
        print("2. 전체 테스트 (모든 테스트)")
        
        choice = input("\n선택 (1/2): ").strip()
        test_type = "basic" if choice == "1" else "full"
    
    # 테스트 실행
    if test_type in ["basic", "1", "--quick"]:
        success = run_basic_tests()
    else:
        success = run_full_tests()
    
    # 결과 출력
    if success:
        print("\n🎉 모든 테스트가 성공했습니다!")
        return 0
    else:
        print("\n❌ 일부 테스트가 실패했습니다.")
        return 1

if __name__ == "__main__":
    exit(main())