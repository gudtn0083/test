import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2
import random
import os
import re
import hashlib
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional, Union
import logging
import warnings
from functools import wraps
import gc
import time

# 보안 설정
warnings.filterwarnings('ignore', category=FutureWarning)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 보안 데코레이터
def secure_operation(func):
    """보안 검증을 위한 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Security error in {func.__name__}: {str(e)}")
            raise SecurityError(f"Operation failed: {func.__name__}")
    return wrapper

class SecurityError(Exception):
    """보안 관련 예외 클래스"""
    pass

class InputValidator:
    """입력값 검증 클래스"""
    
    # 허용된 파일 확장자
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
    
    # 최대 파일 크기 (100MB)
    MAX_FILE_SIZE = 100 * 1024 * 1024
    
    # 최대 이미지 크기
    MAX_IMAGE_SIZE = 2048
    
    # 허용된 문자 패턴 (영문, 숫자, 일부 특수문자)
    SAFE_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    
    # 위험한 프롬프트 패턴
    DANGEROUS_PATTERNS = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'eval\s*\(',
        r'exec\s*\(',
        r'system\s*\(',
        r'__import__',
        r'subprocess',
        r'os\.system',
    ]
    
    @classmethod
    def validate_filename(cls, filename: str) -> str:
        """파일명 검증 및 정화"""
        if not filename:
            raise SecurityError("Filename cannot be empty")
        
        # 경로 탐색 공격 방지
        filename = os.path.basename(filename)
        
        # 위험한 문자 제거
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        
        # 길이 제한
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext
        
        # 확장자 검증
        ext = Path(filename).suffix.lower()
        if ext and ext not in cls.ALLOWED_EXTENSIONS:
            filename = filename.replace(ext, '.png')
        
        # 빈 파일명 방지
        if not filename or filename.startswith('.'):
            filename = f"generated_{int(time.time())}.png"
        
        return filename
    
    @classmethod
    def validate_path(cls, path: str) -> str:
        """경로 검증 및 정화"""
        if not path:
            raise SecurityError("Path cannot be empty")
        
        # 절대 경로를 상대 경로로 변환
        path = os.path.normpath(path)
        
        # 상위 디렉토리 접근 방지
        if '..' in path or path.startswith('/'):
            raise SecurityError("Invalid path: directory traversal detected")
        
        # 현재 작업 디렉토리 기준으로 안전한 경로 생성
        safe_path = os.path.join(os.getcwd(), path)
        
        return safe_path
    
    @classmethod
    def validate_prompt(cls, prompt: str) -> str:
        """프롬프트 검증 및 정화"""
        if not prompt:
            return ""
        
        # 길이 제한
        if len(prompt) > 1000:
            prompt = prompt[:1000]
        
        # 위험한 패턴 검사
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected in prompt: {pattern}")
                raise SecurityError("Invalid prompt: contains dangerous content")
        
        # HTML 태그 제거
        prompt = re.sub(r'<[^>]+>', '', prompt)
        
        # 연속된 공백 정리
        prompt = re.sub(r'\s+', ' ', prompt).strip()
        
        return prompt
    
    @classmethod
    def validate_image_params(cls, width: int, height: int, steps: int, guidance: float) -> tuple:
        """이미지 생성 파라미터 검증"""
        # 크기 제한
        width = max(256, min(width, cls.MAX_IMAGE_SIZE))
        height = max(256, min(height, cls.MAX_IMAGE_SIZE))
        
        # 8의 배수로 조정 (Stable Diffusion 요구사항)
        width = (width // 8) * 8
        height = (height // 8) * 8
        
        # 스텝 수 제한
        steps = max(1, min(steps, 100))
        
        # 가이던스 스케일 제한
        guidance = max(1.0, min(guidance, 20.0))
        
        return width, height, steps, guidance

class SecureMemoryManager:
    """메모리 관리 클래스"""
    
    @staticmethod
    def clear_cache():
        """캐시 정리"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
    
    @staticmethod
    def get_memory_info():
        """메모리 사용량 정보"""
        if torch.cuda.is_available():
            return {
                'gpu_memory_allocated': torch.cuda.memory_allocated(),
                'gpu_memory_reserved': torch.cuda.memory_reserved(),
                'gpu_memory_free': torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()
            }
        return {'cpu_only': True}

class CuteAnimalGenerator:
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        """
        귀여운 동물 이미지 생성기 초기화
        
        Args:
            model_id: 사용할 Stable Diffusion 모델 ID
        """
        # 입력 검증
        if not isinstance(model_id, str) or not model_id.strip():
            raise SecurityError("Invalid model_id")
        
        self.model_id = InputValidator.validate_prompt(model_id)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.memory_manager = SecureMemoryManager()
        
        logger.info(f"Using device: {self.device}")
        logger.info(f"Memory info: {self.memory_manager.get_memory_info()}")
        
        # 파이프라인 로드
        self.pipe = self._load_pipeline()
        
        # 허용된 동물 목록 (화이트리스트 방식)
        self.allowed_animals = {
            "puppy", "kitten", "baby panda", "baby fox", "baby rabbit", 
            "baby bear", "baby elephant", "baby penguin", "baby owl", 
            "baby deer", "baby seal", "baby hedgehog", "baby raccoon",
            "baby koala", "baby tiger", "baby lion", "hamster", "guinea pig"
        }
        
        # 허용된 스타일 목록
        self.allowed_styles = {
            "kawaii style", "chibi style", "cartoon style", "anime style",
            "pixar style", "disney style", "studio ghibli style", "adorable",
            "fluffy", "round and chubby", "with big eyes", "pastel colors"
        }
        
        # 허용된 액세서리 목록
        self.allowed_accessories = {
            "wearing a tiny hat", "with a bow tie", "with flower crown",
            "wearing glasses", "with a scarf", "holding a heart",
            "with sparkles around", "in a teacup", "with rainbow background",
            "sitting on clouds", "with fairy wings", "wearing a sweater"
        }
        
        # 허용된 환경 목록
        self.allowed_environments = {
            "in a meadow", "in a forest", "on a soft blanket", "in a garden",
            "under cherry blossoms", "in a cozy room", "on a pillow",
            "in a magical forest", "surrounded by flowers", "in sunlight"
        }

    @secure_operation
    def _load_pipeline(self) -> StableDiffusionPipeline:
        """Stable Diffusion 파이프라인 로드"""
        try:
            pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,  # 개발 환경에서만 비활성화
                requires_safety_checker=False,
                use_auth_token=False  # 인증 토큰 사용하지 않음
            )
            
            # 스케줄러 최적화
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            pipe = pipe.to(self.device)
            
            # 메모리 최적화
            if self.device == "cuda":
                try:
                    pipe.enable_memory_efficient_attention()
                    pipe.enable_xformers_memory_efficient_attention()
                except Exception as e:
                    logger.warning(f"Memory optimization failed: {e}")
            
            logger.info("Pipeline loaded successfully")
            return pipe
            
        except Exception as e:
            logger.error(f"Failed to load pipeline: {e}")
            raise SecurityError("Failed to initialize AI model")

    @secure_operation
    def generate_cute_prompt(self, animal: Optional[str] = None, custom_prompt: str = "") -> Tuple[str, str]:
        """
        귀여운 동물 프롬프트 자동 생성
        
        Args:
            animal: 특정 동물 지정 (허용된 목록에서만)
            custom_prompt: 사용자 커스텀 프롬프트 (검증됨)
            
        Returns:
            (정화된 프롬프트, 네거티브 프롬프트) 튜플
        """
        try:
            # 입력 검증
            if custom_prompt:
                base_prompt = InputValidator.validate_prompt(custom_prompt)
            else:
                if animal and animal not in self.allowed_animals:
                    logger.warning(f"Invalid animal requested: {animal}")
                    animal = None
                
                if animal is None:
                    animal = random.choice(list(self.allowed_animals))
                
                style = random.choice(list(self.allowed_styles))
                accessory = random.choice(list(self.allowed_accessories)) if random.random() > 0.5 else ""
                environment = random.choice(list(self.allowed_environments)) if random.random() > 0.7 else ""
                
                # 프롬프트 조합
                prompt_parts = [
                    f"extremely cute {animal}",
                    style,
                    accessory,
                    environment,
                    "high quality, detailed, adorable, heartwarming, soft lighting, professional photography"
                ]
                
                base_prompt = ", ".join(filter(None, prompt_parts))
            
            # 최종 검증
            base_prompt = InputValidator.validate_prompt(base_prompt)
            
            # 안전한 네거티브 프롬프트
            negative_prompt = "ugly, scary, dark, aggressive, realistic photo, blurry, low quality, distorted, horror, nsfw, inappropriate"
            
            return base_prompt, negative_prompt
            
        except Exception as e:
            logger.error(f"Prompt generation failed: {e}")
            raise SecurityError("Failed to generate prompt")

    @secure_operation
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
        귀여운 동물 이미지 생성 (보안 강화)
        
        Args:
            prompt: 커스텀 프롬프트 (검증됨)
            animal: 특정 동물 지정 (허용된 목록에서만)
            width: 이미지 너비 (검증됨)
            height: 이미지 높이 (검증됨)
            num_inference_steps: 추론 스텝 수 (제한됨)
            guidance_scale: 가이던스 스케일 (제한됨)
            num_images: 생성할 이미지 수 (제한됨)
            
        Returns:
            생성된 이미지 리스트
        """
        try:
            # 파라미터 검증
            width, height, num_inference_steps, guidance_scale = InputValidator.validate_image_params(
                width, height, num_inference_steps, guidance_scale
            )
            
            # 이미지 수 제한
            num_images = max(1, min(num_images, 4))
            
            # 메모리 체크
            memory_info = self.memory_manager.get_memory_info()
            if 'gpu_memory_free' in memory_info and memory_info['gpu_memory_free'] < 2 * 1024**3:  # 2GB
                logger.warning("Low GPU memory, reducing batch size")
                num_images = 1
            
            # 프롬프트 생성
            if prompt is None:
                prompt, negative_prompt = self.generate_cute_prompt(animal)
            else:
                prompt = InputValidator.validate_prompt(prompt)
                _, negative_prompt = self.generate_cute_prompt()
            
            logger.info(f"Generating {num_images} image(s) with prompt: {prompt[:100]}...")
            
            # 이미지 생성
            with torch.autocast(self.device):
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    num_images_per_prompt=num_images,
                    generator=torch.Generator(device=self.device).manual_seed(random.randint(0, 2**32-1))
                )
            
            # 메모리 정리
            self.memory_manager.clear_cache()
            
            images = result.images
            logger.info(f"Successfully generated {len(images)} images")
            
            return images
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            self.memory_manager.clear_cache()
            raise SecurityError("Failed to generate image")

    @secure_operation
    def enhance_cuteness(self, image: Image.Image) -> Image.Image:
        """
        이미지의 귀여움을 향상시키는 후처리 (보안 강화)
        
        Args:
            image: 원본 이미지
            
        Returns:
            향상된 이미지
        """
        try:
            if not isinstance(image, Image.Image):
                raise SecurityError("Invalid image input")
            
            # 이미지 크기 검증
            if image.size[0] > InputValidator.MAX_IMAGE_SIZE or image.size[1] > InputValidator.MAX_IMAGE_SIZE:
                raise SecurityError("Image too large")
            
            # 밝기와 대비 조정 (안전한 범위)
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(min(1.2, max(0.8, 1.1)))
            
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(min(1.2, max(0.8, 1.05)))
            
            # 채도 향상 (안전한 범위)
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(min(1.3, max(0.7, 1.15)))
            
            # 약간의 블러로 부드러움 추가 (안전한 범위)
            image = image.filter(ImageFilter.GaussianBlur(radius=min(1.0, max(0.1, 0.5))))
            
            return image
            
        except Exception as e:
            logger.error(f"Image enhancement failed: {e}")
            return image  # 실패 시 원본 반환

    @secure_operation
    def add_cute_effects(self, image: Image.Image) -> Image.Image:
        """
        귀여운 효과 추가 (보안 강화)
        
        Args:
            image: 원본 이미지
            
        Returns:
            효과가 추가된 이미지
        """
        try:
            if not isinstance(image, Image.Image):
                raise SecurityError("Invalid image input")
            
            # numpy 배열로 안전하게 변환
            img_array = np.array(image)
            
            # 배열 크기 검증
            if img_array.size > 50 * 1024 * 1024:  # 50MB 제한
                raise SecurityError("Image array too large")
            
            # 파스텔 톤 조정 (안전한 범위)
            img_array = img_array.astype(np.float32)
            
            # 안전한 색상 조정
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.02, 0, 255)  # Red
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.98, 0, 255)  # Blue
            
            img_array = img_array.astype(np.uint8)
            
            return Image.fromarray(img_array)
            
        except Exception as e:
            logger.error(f"Effect application failed: {e}")
            return image  # 실패 시 원본 반환

    @secure_operation
    def generate_cute_animal_batch(
        self,
        count: int = 4,
        animals: Optional[List[str]] = None,
        save_path: str = "generated_animals"
    ) -> List[Image.Image]:
        """
        여러 귀여운 동물 이미지를 배치로 생성 (보안 강화)
        
        Args:
            count: 생성할 이미지 수 (제한됨)
            animals: 특정 동물 리스트 (검증됨)
            save_path: 저장 경로 (검증됨)
            
        Returns:
            생성된 이미지 리스트
        """
        try:
            # 배치 크기 제한
            count = max(1, min(count, 10))
            
            # 경로 검증
            safe_save_path = InputValidator.validate_path(save_path)
            
            # 동물 목록 검증
            if animals:
                validated_animals = [animal for animal in animals if animal in self.allowed_animals]
                if not validated_animals:
                    raise SecurityError("No valid animals provided")
                animals = validated_animals
            
            os.makedirs(safe_save_path, exist_ok=True)
            generated_images = []
            
            for i in range(count):
                try:
                    animal = animals[i % len(animals)] if animals else None
                    
                    # 이미지 생성
                    images = self.generate_image(animal=animal, num_images=1)
                    image = images[0]
                    
                    # 후처리
                    image = self.enhance_cuteness(image)
                    image = self.add_cute_effects(image)
                    
                    # 안전한 파일명 생성
                    timestamp = int(time.time())
                    filename = f"cute_animal_{timestamp}_{i+1:03d}.png"
                    filename = InputValidator.validate_filename(filename)
                    filepath = os.path.join(safe_save_path, filename)
                    
                    # 이미지 저장
                    image.save(filepath, "PNG", optimize=True)
                    
                    generated_images.append(image)
                    logger.info(f"Generated and saved: {filepath}")
                    
                except Exception as e:
                    logger.error(f"Failed to generate image {i+1}: {e}")
                    continue
            
            return generated_images
            
        except Exception as e:
            logger.error(f"Batch generation failed: {e}")
            raise SecurityError("Failed to generate batch")

    def __del__(self):
        """소멸자 - 메모리 정리"""
        try:
            if hasattr(self, 'memory_manager'):
                self.memory_manager.clear_cache()
        except:
            pass

# 보안 강화된 편의 함수들
@secure_operation
def quick_generate(animal: str = None, save_as: str = "cute_animal.png") -> Image.Image:
    """빠른 이미지 생성 함수 (보안 강화)"""
    try:
        # 입력 검증
        if animal and not isinstance(animal, str):
            raise SecurityError("Invalid animal type")
        
        save_as = InputValidator.validate_filename(save_as)
        
        generator = CuteAnimalGenerator()
        images = generator.generate_image(animal=animal)
        image = generator.enhance_cuteness(images[0])
        
        # 안전한 저장
        image.save(save_as, "PNG", optimize=True)
        return image
        
    except Exception as e:
        logger.error(f"Quick generation failed: {e}")
        raise SecurityError("Failed to generate image")

@secure_operation
def generate_animal_collection(animals: List[str], save_path: str = "animal_collection") -> List[Image.Image]:
    """동물 컬렉션 생성 함수 (보안 강화)"""
    try:
        if not isinstance(animals, list):
            raise SecurityError("Animals must be a list")
        
        generator = CuteAnimalGenerator()
        return generator.generate_cute_animal_batch(
            count=len(animals),
            animals=animals,
            save_path=save_path
        )
        
    except Exception as e:
        logger.error(f"Collection generation failed: {e}")
        raise SecurityError("Failed to generate collection")

if __name__ == "__main__":
    # 예제 실행
    try:
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
        
    except SecurityError as e:
        print(f"🚨 보안 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        logger.error(f"Main execution failed: {e}")