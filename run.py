#!/usr/bin/env python3
"""
귀여운 동물 이미지 생성기 - 간단 실행 스크립트
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """필요한 패키지들이 설치되어 있는지 확인"""
    required_packages = [
        'torch', 'diffusers', 'transformers', 'streamlit', 
        'PIL', 'numpy', 'cv2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'cv2':
                import cv2
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 다음 패키지들이 설치되지 않았습니다:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n다음 명령어로 설치해주세요:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def run_web_app():
    """웹 앱 실행"""
    print("🚀 웹 인터페이스를 시작합니다...")
    print("브라우저에서 http://localhost:8501 로 접속하세요!")
    print("종료하려면 Ctrl+C를 누르세요.\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "web_app.py"])
    except KeyboardInterrupt:
        print("\n👋 웹앱이 종료되었습니다.")
    except FileNotFoundError:
        print("❌ streamlit이 설치되지 않았습니다.")
        print("pip install streamlit으로 설치해주세요.")

def run_cli_example():
    """CLI 예제 실행"""
    print("🎨 CLI로 귀여운 강아지를 생성합니다...")
    
    try:
        subprocess.run([
            sys.executable, "cli_generator.py", 
            "--animal", "puppy", 
            "--output", "example_puppy.png",
            "--size", "512"
        ])
        print("✅ example_puppy.png 파일이 생성되었습니다!")
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")

def run_python_example():
    """Python 코드 예제 실행"""
    print("🐍 Python 코드로 귀여운 고양이를 생성합니다...")
    
    try:
        from cute_animal_generator import quick_generate
        print("모델을 로딩 중입니다...")
        image = quick_generate(animal="kitten", save_as="example_kitten.png")
        print("✅ example_kitten.png 파일이 생성되었습니다!")
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")

def show_menu():
    """메뉴 표시"""
    print("""
🐾 귀여운 동물 AI 이미지 생성기 🐾

실행 옵션을 선택하세요:

1. 웹 인터페이스 실행 (추천!)
2. CLI 예제 실행 (강아지 생성)
3. Python 예제 실행 (고양이 생성)
4. 의존성 확인
5. 종료

""")

def main():
    while True:
        show_menu()
        
        try:
            choice = input("선택 (1-5): ").strip()
            
            if choice == "1":
                if check_dependencies():
                    run_web_app()
                break
                
            elif choice == "2":
                if check_dependencies():
                    run_cli_example()
                input("\nEnter를 눌러 메뉴로 돌아가기...")
                
            elif choice == "3":
                if check_dependencies():
                    run_python_example()
                input("\nEnter를 눌러 메뉴로 돌아가기...")
                
            elif choice == "4":
                print("📦 의존성을 확인 중입니다...")
                if check_dependencies():
                    print("✅ 모든 필요한 패키지가 설치되어 있습니다!")
                input("\nEnter를 눌러 메뉴로 돌아가기...")
                
            elif choice == "5":
                print("👋 프로그램을 종료합니다.")
                break
                
            else:
                print("❌ 잘못된 선택입니다. 1-5 사이의 숫자를 입력해주세요.")
                
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()