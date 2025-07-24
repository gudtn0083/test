#!/usr/bin/env python3
"""
귀여운 동물 이미지 생성기 - 명령행 인터페이스
"""

import argparse
import sys
import os
from pathlib import Path
from cute_animal_generator import CuteAnimalGenerator, quick_generate, generate_animal_collection

def main():
    parser = argparse.ArgumentParser(
        description="🐾 귀여운 동물 AI 이미지 생성기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제 사용법:
  %(prog)s --animal puppy --output my_puppy.png
  %(prog)s --animal "baby panda" --style kawaii --size 768
  %(prog)s --prompt "cute kitten with rainbow background" 
  %(prog)s --batch --count 5 --animals puppy kitten "baby fox"
  %(prog)s --random --count 3
        """
    )
    
    # 기본 옵션
    parser.add_argument(
        "--animal", "-a",
        type=str,
        help="생성할 동물 종류 (예: puppy, kitten, baby panda)"
    )
    
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        help="커스텀 프롬프트"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="cute_animal.png",
        help="출력 파일명 (기본값: cute_animal.png)"
    )
    
    # 스타일 옵션
    parser.add_argument(
        "--style", "-s",
        type=str,
        choices=["kawaii", "chibi", "cartoon", "anime", "pixar", "disney", "ghibli"],
        help="이미지 스타일"
    )
    
    # 크기 옵션
    parser.add_argument(
        "--size",
        type=int,
        choices=[512, 768, 1024],
        default=512,
        help="이미지 크기 (기본값: 512)"
    )
    
    # 품질 옵션
    parser.add_argument(
        "--steps",
        type=int,
        default=20,
        help="생성 스텝 수 (기본값: 20, 높을수록 품질 향상)"
    )
    
    parser.add_argument(
        "--guidance",
        type=float,
        default=7.5,
        help="가이던스 스케일 (기본값: 7.5)"
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
        help="배치 모드에서 생성할 이미지 수 (기본값: 4)"
    )
    
    parser.add_argument(
        "--animals",
        nargs="+",
        help="배치 모드에서 생성할 동물들의 리스트"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated_animals",
        help="배치 모드 출력 디렉토리 (기본값: generated_animals)"
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
    
    args = parser.parse_args()
    
    # 동물 목록 표시
    if args.list_animals:
        print("🐾 사용 가능한 동물들:")
        animals = [
            "puppy", "kitten", "baby panda", "baby fox", "baby rabbit",
            "baby bear", "baby elephant", "baby penguin", "baby owl",
            "baby deer", "baby seal", "baby hedgehog", "baby raccoon",
            "baby koala", "baby tiger", "baby lion", "hamster", "guinea pig"
        ]
        for animal in animals:
            print(f"  - {animal}")
        return
    
    try:
        # AI 생성기 초기화
        print("🤖 AI 모델을 로딩 중입니다...")
        generator = CuteAnimalGenerator()
        print("✅ 모델 로딩 완료!")
        
        if args.batch:
            # 배치 모드
            print(f"🎪 {args.count}마리의 귀여운 동물들을 생성 중입니다...")
            
            animals = args.animals if args.animals else None
            images = generator.generate_cute_animal_batch(
                count=args.count,
                animals=animals,
                save_path=args.output_dir
            )
            
            print(f"✨ {len(images)}마리의 귀여운 동물들이 '{args.output_dir}' 폴더에 저장되었습니다!")
            
        else:
            # 단일 이미지 모드
            print("🎨 귀여운 동물을 생성 중입니다...")
            
            # 프롬프트 구성
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
            
            # 저장
            image.save(args.output)
            print(f"✨ 귀여운 동물이 '{args.output}'에 저장되었습니다!")
            
            # 이미지 정보 출력
            print(f"📊 이미지 정보:")
            print(f"   크기: {image.size[0]}x{image.size[1]}")
            print(f"   파일: {args.output}")
            print(f"   크기: {os.path.getsize(args.output) / 1024:.1f} KB")
            
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()