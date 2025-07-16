#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한국어 텍스트 추출 도구
Korean Text Extraction Tool

지원하는 OCR 엔진:
1. EasyOCR - 한국어 지원이 우수
2. Tesseract OCR - 전통적인 OCR 엔진
3. PaddleOCR - 중국에서 개발된 다국어 OCR

사용 방법:
python text_extractor.py image_path.png
"""

import os
import sys
import argparse
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextExtractor:
    def __init__(self):
        self.easyocr_available = False
        self.tesseract_available = False
        self.paddleocr_available = False
        
        # OCR 엔진 초기화
        self._init_engines()
    
    def _init_engines(self):
        """OCR 엔진들을 초기화합니다."""
        
        # EasyOCR 초기화
        try:
            import easyocr
            self.easyocr_reader = easyocr.Reader(['ko', 'en'])
            self.easyocr_available = True
            logger.info("EasyOCR 초기화 완료")
        except ImportError:
            logger.warning("EasyOCR를 사용할 수 없습니다. 설치하려면: pip install easyocr")
        
        # Tesseract OCR 초기화
        try:
            import pytesseract
            # Tesseract 경로 설정 (필요시)
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.pytesseract = pytesseract
            self.tesseract_available = True
            logger.info("Tesseract OCR 초기화 완료")
        except ImportError:
            logger.warning("Tesseract OCR를 사용할 수 없습니다. 설치하려면: pip install pytesseract")
        
        # PaddleOCR 초기화
        try:
            from paddleocr import PaddleOCR
            self.paddleocr = PaddleOCR(use_angle_cls=True, lang='korean')
            self.paddleocr_available = True
            logger.info("PaddleOCR 초기화 완료")
        except ImportError:
            logger.warning("PaddleOCR를 사용할 수 없습니다. 설치하려면: pip install paddleocr")
    
    def preprocess_image(self, image_path):
        """이미지 전처리를 수행합니다."""
        try:
            # 이미지 읽기
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")
            
            # 그레이스케일 변환
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 노이즈 제거
            denoised = cv2.medianBlur(gray, 5)
            
            # 대비 향상
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # 이진화
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary, image
            
        except Exception as e:
            logger.error(f"이미지 전처리 중 오류 발생: {e}")
            return None, None
    
    def extract_with_easyocr(self, image_path):
        """EasyOCR을 사용하여 텍스트를 추출합니다."""
        if not self.easyocr_available:
            return None
        
        try:
            results = self.easyocr_reader.readtext(str(image_path))
            
            extracted_text = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # 신뢰도 50% 이상만 포함
                    extracted_text.append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
            
            return {
                'engine': 'EasyOCR',
                'results': extracted_text,
                'full_text': '\n'.join([item['text'] for item in extracted_text])
            }
            
        except Exception as e:
            logger.error(f"EasyOCR 텍스트 추출 중 오류: {e}")
            return None
    
    def extract_with_tesseract(self, image_path):
        """Tesseract OCR을 사용하여 텍스트를 추출합니다."""
        if not self.tesseract_available:
            return None
        
        try:
            # 전처리된 이미지 사용
            processed_image, _ = self.preprocess_image(image_path)
            if processed_image is None:
                return None
            
            # 한국어 + 영어 설정
            config = '--oem 3 --psm 6 -l kor+eng'
            
            # 텍스트 추출
            text = self.pytesseract.image_to_string(processed_image, config=config)
            
            # 상세 정보 추출
            data = self.pytesseract.image_to_data(processed_image, config=config, output_type=self.pytesseract.Output.DICT)
            
            detailed_results = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30:  # 신뢰도 30% 이상
                    word = data['text'][i].strip()
                    if word:
                        detailed_results.append({
                            'text': word,
                            'confidence': int(data['conf'][i]) / 100.0,
                            'bbox': (data['left'][i], data['top'][i], 
                                   data['left'][i] + data['width'][i], 
                                   data['top'][i] + data['height'][i])
                        })
            
            return {
                'engine': 'Tesseract',
                'results': detailed_results,
                'full_text': text.strip()
            }
            
        except Exception as e:
            logger.error(f"Tesseract 텍스트 추출 중 오류: {e}")
            return None
    
    def extract_with_paddleocr(self, image_path):
        """PaddleOCR을 사용하여 텍스트를 추출합니다."""
        if not self.paddleocr_available:
            return None
        
        try:
            results = self.paddleocr.ocr(str(image_path), cls=True)
            
            extracted_text = []
            for line in results[0]:
                bbox, (text, confidence) = line
                if confidence > 0.5:  # 신뢰도 50% 이상만 포함
                    extracted_text.append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
            
            return {
                'engine': 'PaddleOCR',
                'results': extracted_text,
                'full_text': '\n'.join([item['text'] for item in extracted_text])
            }
            
        except Exception as e:
            logger.error(f"PaddleOCR 텍스트 추출 중 오류: {e}")
            return None
    
    def extract_text(self, image_path, engines=None):
        """지정된 엔진들을 사용하여 텍스트를 추출합니다."""
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")
        
        if engines is None:
            engines = ['easyocr', 'tesseract', 'paddleocr']
        
        results = {}
        
        # EasyOCR
        if 'easyocr' in engines:
            logger.info("EasyOCR로 텍스트 추출 중...")
            result = self.extract_with_easyocr(image_path)
            if result:
                results['easyocr'] = result
        
        # Tesseract
        if 'tesseract' in engines:
            logger.info("Tesseract로 텍스트 추출 중...")
            result = self.extract_with_tesseract(image_path)
            if result:
                results['tesseract'] = result
        
        # PaddleOCR
        if 'paddleocr' in engines:
            logger.info("PaddleOCR로 텍스트 추출 중...")
            result = self.extract_with_paddleocr(image_path)
            if result:
                results['paddleocr'] = result
        
        return results
    
    def save_results(self, results, output_path):
        """결과를 파일로 저장합니다."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=== 텍스트 추출 결과 ===\n\n")
            
            for engine_name, result in results.items():
                f.write(f"--- {result['engine']} 결과 ---\n")
                f.write(f"추출된 텍스트:\n{result['full_text']}\n\n")
                
                f.write("상세 정보:\n")
                for item in result['results']:
                    f.write(f"텍스트: {item['text']}\n")
                    f.write(f"신뢰도: {item['confidence']:.2f}\n")
                    f.write(f"위치: {item['bbox']}\n\n")
                
                f.write("-" * 50 + "\n\n")

def main():
    parser = argparse.ArgumentParser(description='한국어 텍스트 추출 도구')
    parser.add_argument('image_path', help='추출할 이미지 파일 경로')
    parser.add_argument('--engines', nargs='+', 
                       choices=['easyocr', 'tesseract', 'paddleocr'],
                       default=['easyocr', 'tesseract', 'paddleocr'],
                       help='사용할 OCR 엔진 선택')
    parser.add_argument('--output', '-o', 
                       help='결과를 저장할 파일 경로')
    
    args = parser.parse_args()
    
    # 텍스트 추출기 생성
    extractor = TextExtractor()
    
    try:
        # 텍스트 추출
        logger.info(f"이미지에서 텍스트 추출 시작: {args.image_path}")
        results = extractor.extract_text(args.image_path, args.engines)
        
        if not results:
            logger.error("텍스트를 추출할 수 없습니다.")
            return
        
        # 결과 출력
        print("\n=== 텍스트 추출 결과 ===\n")
        
        for engine_name, result in results.items():
            print(f"--- {result['engine']} ---")
            print(f"추출된 텍스트:\n{result['full_text']}")
            print(f"추출된 항목 수: {len(result['results'])}")
            print("-" * 40)
        
        # 파일로 저장
        if args.output:
            extractor.save_results(results, args.output)
            logger.info(f"결과가 저장되었습니다: {args.output}")
        
    except Exception as e:
        logger.error(f"오류 발생: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())