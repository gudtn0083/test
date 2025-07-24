#!/usr/bin/env python3
"""
귀여운 동물 이미지 생성기 - 명령행 인터페이스 (보안 강화)
"""

import argparse
import sys
import os
import re
import logging
from pathlib import Path
from typing import List, Optional
from cute_animal_generator import (
    CuteAnimalGenerator, 
    quick_generate, 
    generate_animal_collection, 
    SecurityError, 
    InputValidator
)

# 보안 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cli.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CLISecurity:
    """CLI 보안 관리 클래스"""
    
    # 허용된 동물 목록 (화이트리스트)
    ALLOWED_ANIMALS = {
        "puppy", "kitten", "baby panda", "baby fox", "baby rabbit",
        "baby bear", "baby elephant", "baby penguin", "baby owl",
        "baby deer", "baby seal", "baby hedgehog", "baby raccoon",
        "baby koala", "baby tiger", "baby lion", "hamster", "guinea pig"
    }
    
    # 허용된 스타일 목록
    ALLOWED_STYLES = {
        "kawaii", "chibi", "cartoon", "anime", "pixar", "disney", "ghibli"
    }
    
    # 최대 배치 크기
    MAX_BATCH_SIZE = 10
    
    # 최대 파일명 길이
    MAX_FILENAME_LENGTH = 200
    
    @staticmethod
    def validate_animal(animal: str) -> bool:
        """동물 이름 검증"""
        return animal.lower() in CLISecurity.ALLOWED_ANIMALS
    
    @staticmethod
    def validate_style(style: str) -> bool:
        """스타일 검증"""
        return style.lower() in CLISecurity.ALLOWED_STYLES
    
    @staticmethod
    def sanitize_path(path: str) -> str:
        """경로 정화 및 검증"""
        try:
            return InputValidator.validate_path(path)
        except SecurityError as e:
            logger.error(f"Path validation failed: {e}")
            raise
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """파일명 정화 및 검증"""
        try:
            return InputValidator.validate_filename(filename)
        except SecurityError as e:
            logger.error(f"Filename validation failed: {e}")
            raise
    
    @staticmethod
    def validate_count(count: int) -> int:
        """배치 카운트 검증"""
        if not isinstance(count, int) or count < 1:
            raise SecurityError("Count must be a positive integer")
        
        if count > CLISecurity.MAX_BATCH_SIZE:
            logger.warning(f"Count {count} exceeds maximum {CLISecurity.MAX_BATCH_SIZE}, limiting")
            return CLISecurity.MAX_BATCH_SIZE
        
        return count

def create_secure_parser() -> argparse.ArgumentParser:
    """보안 강화된 argument parser 생성"""
    parser = argparse.ArgumentParser(
        description="🐾 귀여운 동물 AI 이미지 생성기 (보안 강화)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
보안 강화 예제 사용법:
  %(prog)s --animal puppy --output my_puppy.png
  %(prog)s --animal "baby panda" --style kawaii --size 768
  %(prog)s --prompt "cute kitten with rainbow background" 
  %(prog)s --batch --count 5 --animals puppy kitten "baby fox"
  %(prog)s --random --count 3

보안 기능:
  - 입력값 자동 검증 및 정화
  - 경로 탐색 공격 방지
  - 파일명 위험 문자 제거
  - 파라미터 안전 범위 제한
        """
    )
    
    # 기본 옵션
    parser.add_argument(
        "--animal", "-a",
        type=str,
        help=f"생성할 동물 종류 (허용된 동물: {', '.join(sorted(CLISecurity.ALLOWED_ANIMALS))})"
    )
    
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        help="커스텀 프롬프트 (최대 1000자, 자동 정화됨)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="cute_animal.png",
        help="출력 파일명 (자동 정화됨, 기본값: cute_animal.png)"
    )
    
    # 스타일 옵션 (제한된 선택지)
    parser.add_argument(
        "--style", "-s",
        type=str,
        choices=list(CLISecurity.ALLOWED_STYLES),
        help="이미지 스타일 (화이트리스트 방식)"
    )
    
    # 크기 옵션 (안전한 범위)
    parser.add_argument(
        "--size",
        type=int,
        choices=[256, 512, 768, 1024],
        default=512,
        help="이미지 크기 (허용된 크기만 선택 가능, 기본값: 512)"
    )
    
    # 품질 옵션 (제한된 범위)
    parser.add_argument(
        "--steps",
        type=int,
        default=20,
        help="생성 스텝 수 (1-100, 기본값: 20)"
    )
    
    parser.add_argument(
        "--guidance",
        type=float,
        default=7.5,
        help="가이던스 스케일 (1.0-20.0, 기본값: 7.5)"
    )
    
    # 배치 옵션
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="배치 모드 활성화"
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=4,
        help=f"배치 모드에서 생성할 이미지 수 (최대 {CLISecurity.MAX_BATCH_SIZE}, 기본값: 4)"
    )
    
    parser.add_argument(
        "--animals",
        nargs="+",
        help="배치 모드에서 생성할 동물들의 리스트 (허용된 동물만)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated_animals",
        help="배치 모드 출력 디렉토리 (자동 정화됨, 기본값: generated_animals)"
    )
    
    # 기타 옵션
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="랜덤 동물 생성"
    )
    
    parser.add_argument(
        "--enhance",
        action="store_true",
        default=True,
        help="귀여움 향상 효과 적용 (기본값: True)"
    )
    
    parser.add_argument(
        "--list-animals",
        action="store_true",
        help="사용 가능한 동물 목록 표시"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="상세 로그 출력"
    )
    
    return parser

def validate_and_sanitize_args(args) -> argparse.Namespace:
    """인수 검증 및 정화"""
    try:
        # 동물 검증
        if args.animal and not CLISecurity.validate_animal(args.animal):
            logger.error(f"Invalid animal: {args.animal}")
            print(f"❌ 허용되지 않은 동물입니다: {args.animal}")
            print(f"허용된 동물: {', '.join(sorted(CLISecurity.ALLOWED_ANIMALS))}")
            sys.exit(1)
        
        # 스타일 검증 (이미 choices로 제한되어 있음)
        
        # 프롬프트 정화
        if args.prompt:
            try:
                args.prompt = InputValidator.validate_prompt(args.prompt)
            except SecurityError as e:
                logger.error(f"Invalid prompt: {e}")
                print("❌ 프롬프트에 부적절한 내용이 포함되어 있습니다.")
                sys.exit(1)
        
        # 출력 파일명 정화
        try:
            args.output = CLISecurity.sanitize_filename(args.output)
        except SecurityError as e:
            logger.error(f"Invalid output filename: {e}")
            print("❌ 출력 파일명이 유효하지 않습니다.")
            sys.exit(1)
        
        # 출력 디렉토리 정화
        try:
            args.output_dir = CLISecurity.sanitize_path(args.output_dir)
        except SecurityError as e:
            logger.error(f"Invalid output directory: {e}")
            print("❌ 출력 디렉토리가 유효하지 않습니다.")
            sys.exit(1)
        
        # 파라미터 범위 검증
        args.steps = max(1, min(args.steps, 100))
        args.guidance = max(1.0, min(args.guidance, 20.0))
        
        # 배치 카운트 검증
        if args.batch:
            args.count = CLISecurity.validate_count(args.count)
        
        # 동물 리스트 검증
        if args.animals:
            valid_animals = []
            for animal in args.animals:
                if CLISecurity.validate_animal(animal):
                    valid_animals.append(animal)
                else:
                    logger.warning(f"Skipping invalid animal: {animal}")
                    print(f"⚠️ 무시되는 동물: {animal} (허용되지 않음)")
            
            if not valid_animals:
                logger.error("No valid animals provided")
                print("❌ 유효한 동물이 없습니다.")
                sys.exit(1)
            
            args.animals = valid_animals
        
        return args
        
    except Exception as e:
        logger.error(f"Argument validation failed: {e}")
        print(f"❌ 인수 검증 실패: {e}")
        sys.exit(1)

def secure_main():
    """보안 강화된 메인 함수"""
    try:
        parser = create_secure_parser()
        args = parser.parse_args()
        
        # 로깅 레벨 설정
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # 동물 목록 표시
        if args.list_animals:
            print("🐾 사용 가능한 동물들:")
            for animal in sorted(CLISecurity.ALLOWED_ANIMALS):
                print(f"  - {animal}")
            return
        
        # 인수 검증 및 정화
        args = validate_and_sanitize_args(args)
        
        logger.info(f"Starting generation with sanitized args")
        
        # AI 생성기 초기화
        print("🤖 AI 모델을 로딩 중입니다...")
        generator = CuteAnimalGenerator()
        print("✅ 모델 로딩 완료!")
        
        if args.batch:
            # 배치 모드 (보안 강화)
            print(f"🎪 {args.count}마리의 귀여운 동물들을 생성 중입니다...")
            
            try:
                animals = args.animals if args.animals else None
                images = generator.generate_cute_animal_batch(
                    count=args.count,
                    animals=animals,
                    save_path=args.output_dir
                )
                
                print(f"✨ {len(images)}마리의 귀여운 동물들이 '{args.output_dir}' 폴더에 저장되었습니다!")
                
            except SecurityError as e:
                logger.error(f"Security error in batch mode: {e}")
                print(f"🚨 보안 오류: {e}")
                sys.exit(1)
            
        else:
            # 단일 이미지 모드 (보안 강화)
            print("🎨 귀여운 동물을 생성 중입니다...")
            
            try:
                # 파라미터 검증이 완료된 상태에서 이미지 생성
                if args.prompt:
                    prompt = args.prompt
                    if args.style:
                        prompt += f", {args.style} style"
                    images = generator.generate_image(
                        prompt=prompt,
                        width=args.size,
                        height=args.size,
                        num_inference_steps=args.steps,
                        guidance_scale=args.guidance
                    )
                else:
                    animal = args.animal if not args.random else None
                    images = generator.generate_image(
                        animal=animal,
                        width=args.size,
                        height=args.size,
                        num_inference_steps=args.steps,
                        guidance_scale=args.guidance
                    )
                
                # 후처리
                image = images[0]
                if args.enhance:
                    image = generator.enhance_cuteness(image)
                    image = generator.add_cute_effects(image)
                
                # 안전한 저장
                image.save(args.output, "PNG", optimize=True)
                print(f"✨ 귀여운 동물이 '{args.output}'에 저장되었습니다!")
                
                # 파일 정보 출력
                file_size = os.path.getsize(args.output)
                print(f"📊 이미지 정보:")
                print(f"   크기: {image.size[0]}x{image.size[1]}")
                print(f"   파일: {args.output}")
                print(f"   크기: {file_size / 1024:.1f} KB")
                
            except SecurityError as e:
                logger.error(f"Security error in single mode: {e}")
                print(f"🚨 보안 오류: {e}")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except SecurityError as e:
        logger.error(f"Security error: {e}")
        print(f"🚨 보안 오류: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    secure_main()