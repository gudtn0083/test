#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 한국어 텍스트 추출 도구
Simple Korean Text Extractor

사용법:
python simple_text_extractor.py
"""

import cv2
import numpy as np
from PIL import Image
import os

def extract_text_simple(image_path):
    """
    간단한 텍스트 추출 함수
    EasyOCR을 우선적으로 사용하고, 없으면 Tesseract 사용
    """
    
    # EasyOCR 시도
    try:
        import easyocr
        print("EasyOCR로 텍스트 추출 중...")
        
        reader = easyocr.Reader(['ko', 'en'])
        results = reader.readtext(image_path)
        
        extracted_texts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.3:  # 신뢰도 30% 이상
                extracted_texts.append(text)
        
        return '\n'.join(extracted_texts)
        
    except ImportError:
        print("EasyOCR가 설치되지 않았습니다. Tesseract를 시도합니다...")
        
        # Tesseract 시도
        try:
            import pytesseract
            from PIL import Image
            
            print("Tesseract OCR로 텍스트 추출 중...")
            
            # 이미지 열기
            image = Image.open(image_path)
            
            # 한국어 + 영어로 텍스트 추출
            text = pytesseract.image_to_string(image, lang='kor+eng')
            
            return text.strip()
            
        except ImportError:
            return "OCR 라이브러리가 설치되지 않았습니다. pip install easyocr 또는 pip install pytesseract를 실행하세요."
        except Exception as e:
            return f"텍스트 추출 중 오류 발생: {e}"
    
    except Exception as e:
        return f"텍스트 추출 중 오류 발생: {e}"

def main():
    """메인 함수"""
    
    print("=== 간단한 한국어 텍스트 추출 도구 ===\n")
    
    # 현재 디렉토리의 이미지 파일 목록 표시
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    image_files = []
    
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    if image_files:
        print("현재 디렉토리의 이미지 파일들:")
        for i, file in enumerate(image_files, 1):
            print(f"{i}. {file}")
        print()
    
    # 사용자로부터 이미지 파일 경로 입력받기
    while True:
        if image_files:
            choice = input("이미지 파일 번호를 선택하거나 직접 경로를 입력하세요: ")
            
            # 숫자가 입력된 경우
            if choice.isdigit() and 1 <= int(choice) <= len(image_files):
                image_path = image_files[int(choice) - 1]
                break
            # 파일 경로가 입력된 경우
            elif os.path.exists(choice):
                image_path = choice
                break
            else:
                print("올바른 선택이 아닙니다. 다시 시도하세요.")
        else:
            image_path = input("이미지 파일 경로를 입력하세요: ")
            if os.path.exists(image_path):
                break
            else:
                print("파일을 찾을 수 없습니다. 다시 시도하세요.")
    
    # 텍스트 추출
    print(f"\n'{image_path}'에서 텍스트 추출 중...\n")
    extracted_text = extract_text_simple(image_path)
    
    # 결과 출력
    print("=" * 50)
    print("추출된 텍스트:")
    print("=" * 50)
    print(extracted_text)
    print("=" * 50)
    
    # 결과를 파일로 저장할지 묻기
    save_choice = input("\n결과를 파일로 저장하시겠습니까? (y/n): ")
    if save_choice.lower() in ['y', 'yes', '예', 'ㅇ']:
        output_file = f"extracted_text_{os.path.splitext(os.path.basename(image_path))[0]}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"이미지 파일: {image_path}\n")
            f.write("=" * 50 + "\n")
            f.write("추출된 텍스트:\n")
            f.write("=" * 50 + "\n")
            f.write(extracted_text)
        
        print(f"결과가 '{output_file}'에 저장되었습니다.")

if __name__ == "__main__":
    main()