import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2
import random
import os
from typing import List, Tuple, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CuteAnimalGenerator:
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        """
        귀여운 동물 이미지 생성기 초기화
        
        Args:
            model_id: 사용할 Stable Diffusion 모델 ID
        """
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # 파이프라인 로드
        self.pipe = self._load_pipeline()
        
        # 귀여운 동물 프롬프트 템플릿
        self.animal_types = [
            "puppy", "kitten", "baby panda", "baby fox", "baby rabbit", 
            "baby bear", "baby elephant", "baby penguin", "baby owl", 
            "baby deer", "baby seal", "baby hedgehog", "baby raccoon",
            "baby koala", "baby tiger", "baby lion", "hamster", "guinea pig"
        ]
        
        self.cute_styles = [
            "kawaii style", "chibi style", "cartoon style", "anime style",
            "pixar style", "disney style", "studio ghibli style", "adorable",
            "fluffy", "round and chubby", "with big eyes", "pastel colors"
        ]
        
        self.cute_accessories = [
            "wearing a tiny hat", "with a bow tie", "with flower crown",
            "wearing glasses", "with a scarf", "holding a heart",
            "with sparkles around", "in a teacup", "with rainbow background",
            "sitting on clouds", "with fairy wings", "wearing a sweater"
        ]
        
        self.environments = [
            "in a meadow", "in a forest", "on a soft blanket", "in a garden",
            "under cherry blossoms", "in a cozy room", "on a pillow",
            "in a magical forest", "surrounded by flowers", "in sunlight"
        ]

    def _load_pipeline(self) -> StableDiffusionPipeline:
        """Stable Diffusion 파이프라인 로드"""
        try:
            pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # 스케줄러 최적화
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            pipe = pipe.to(self.device)
            
            # 메모리 최적화
            if self.device == "cuda":
                pipe.enable_memory_efficient_attention()
                pipe.enable_xformers_memory_efficient_attention()
            
            logger.info("Pipeline loaded successfully")
            return pipe
            
        except Exception as e:
            logger.error(f"Failed to load pipeline: {e}")
            raise

    def generate_cute_prompt(self, animal: Optional[str] = None, custom_prompt: str = "") -> str:
        """
        귀여운 동물 프롬프트 자동 생성
        
        Args:
            animal: 특정 동물 지정 (None이면 랜덤)
            custom_prompt: 사용자 커스텀 프롬프트
            
        Returns:
            생성된 프롬프트 문자열
        """
        if custom_prompt:
            base_prompt = custom_prompt
        else:
            if animal is None:
                animal = random.choice(self.animal_types)
            
            style = random.choice(self.cute_styles)
            accessory = random.choice(self.cute_accessories) if random.random() > 0.5 else ""
            environment = random.choice(self.environments) if random.random() > 0.7 else ""
            
            # 프롬프트 조합
            prompt_parts = [
                f"extremely cute {animal}",
                style,
                accessory,
                environment,
                "high quality, detailed, adorable, heartwarming, soft lighting, professional photography"
            ]
            
            base_prompt = ", ".join(filter(None, prompt_parts))
        
        # 네거티브 프롬프트
        negative_prompt = "ugly, scary, dark, aggressive, realistic photo, blurry, low quality, distorted, horror"
        
        return base_prompt, negative_prompt

    def generate_image(
        self,
        prompt: Optional[str] = None,
        animal: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        num_images: int = 1
    ) -> List[Image.Image]:
        """
        귀여운 동물 이미지 생성
        
        Args:
            prompt: 커스텀 프롬프트 (None이면 자동 생성)
            animal: 특정 동물 지정
            width: 이미지 너비
            height: 이미지 높이
            num_inference_steps: 추론 스텝 수
            guidance_scale: 가이던스 스케일
            num_images: 생성할 이미지 수
            
        Returns:
            생성된 이미지 리스트
        """
        try:
            # 프롬프트 생성
            if prompt is None:
                prompt, negative_prompt = self.generate_cute_prompt(animal)
            else:
                _, negative_prompt = self.generate_cute_prompt()
            
            logger.info(f"Generating image with prompt: {prompt}")
            
            # 이미지 생성
            with torch.autocast(self.device):
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    num_images_per_prompt=num_images
                )
            
            images = result.images
            logger.info(f"Successfully generated {len(images)} images")
            
            return images
            
        except Exception as e:
            logger.error(f"Failed to generate image: {e}")
            raise

    def enhance_cuteness(self, image: Image.Image) -> Image.Image:
        """
        이미지의 귀여움을 향상시키는 후처리
        
        Args:
            image: 원본 이미지
            
        Returns:
            향상된 이미지
        """
        try:
            # 밝기와 대비 조정
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.05)
            
            # 채도 향상
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.15)
            
            # 약간의 블러로 부드러움 추가
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            return image
            
        except Exception as e:
            logger.error(f"Failed to enhance image: {e}")
            return image

    def add_cute_effects(self, image: Image.Image) -> Image.Image:
        """
        귀여운 효과 추가 (하트, 반짝임 등)
        
        Args:
            image: 원본 이미지
            
        Returns:
            효과가 추가된 이미지
        """
        try:
            # numpy 배열로 변환
            img_array = np.array(image)
            
            # 파스텔 톤 조정
            img_array = img_array.astype(np.float32)
            
            # 약간의 핑크 톤 추가
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.02, 0, 255)  # Red
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.98, 0, 255)  # Blue
            
            img_array = img_array.astype(np.uint8)
            
            return Image.fromarray(img_array)
            
        except Exception as e:
            logger.error(f"Failed to add effects: {e}")
            return image

    def generate_cute_animal_batch(
        self,
        count: int = 4,
        animals: Optional[List[str]] = None,
        save_path: str = "generated_animals"
    ) -> List[Image.Image]:
        """
        여러 귀여운 동물 이미지를 배치로 생성
        
        Args:
            count: 생성할 이미지 수
            animals: 특정 동물 리스트 (None이면 랜덤)
            save_path: 저장 경로
            
        Returns:
            생성된 이미지 리스트
        """
        try:
            os.makedirs(save_path, exist_ok=True)
            generated_images = []
            
            for i in range(count):
                animal = animals[i % len(animals)] if animals else None
                
                # 이미지 생성
                images = self.generate_image(animal=animal, num_images=1)
                image = images[0]
                
                # 후처리
                image = self.enhance_cuteness(image)
                image = self.add_cute_effects(image)
                
                # 저장
                filename = f"cute_animal_{i+1:03d}.png"
                filepath = os.path.join(save_path, filename)
                image.save(filepath)
                
                generated_images.append(image)
                logger.info(f"Generated and saved: {filepath}")
            
            return generated_images
            
        except Exception as e:
            logger.error(f"Failed to generate batch: {e}")
            raise

# 편의 함수들
def quick_generate(animal: str = None, save_as: str = "cute_animal.png") -> Image.Image:
    """빠른 이미지 생성 함수"""
    generator = CuteAnimalGenerator()
    images = generator.generate_image(animal=animal)
    image = generator.enhance_cuteness(images[0])
    image.save(save_as)
    return image

def generate_animal_collection(animals: List[str], save_path: str = "animal_collection") -> List[Image.Image]:
    """동물 컬렉션 생성 함수"""
    generator = CuteAnimalGenerator()
    return generator.generate_cute_animal_batch(
        count=len(animals),
        animals=animals,
        save_path=save_path
    )

if __name__ == "__main__":
    # 예제 실행
    print("🐾 귀여운 동물 이미지 생성기 시작! 🐾")
    
    generator = CuteAnimalGenerator()
    
    # 단일 이미지 생성 예제
    print("단일 이미지 생성 중...")
    images = generator.generate_image(animal="puppy")
    enhanced_image = generator.enhance_cuteness(images[0])
    enhanced_image.save("cute_puppy.png")
    print("✅ cute_puppy.png 저장 완료!")
    
    # 배치 생성 예제
    print("배치 이미지 생성 중...")
    batch_images = generator.generate_cute_animal_batch(count=3)
    print("✅ 배치 생성 완료!")
    
    print("🎉 모든 이미지 생성이 완료되었습니다!")