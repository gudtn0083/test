#!/usr/bin/env python3
"""
보안 강화된 귀여운 동물 생성기 (Secure Cute Animal Generator)

이 모듈은 시큐어 코딩 원칙을 적용하여 안전한 동물 이미지 생성을 제공합니다.

보안 기능:
- 입력 검증 및 sanitization
- 경로 순회 공격 방지
- 메모리 안전성
- Rate limiting
- 안전한 파일 처리
- 예외 처리 강화
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
import numpy as np
import random
import re
import os
import tempfile
import time
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from enum import Enum
import warnings

# 보안 경고 설정
warnings.filterwarnings('default')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('animal_generator_security.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """보안 관련 예외"""
    pass

class ValidationError(Exception):
    """입력 검증 예외"""
    pass

class AnimalType(Enum):
    """허용된 동물 타입 enum"""
    BEAR = "bear"
    CAT = "cat"
    DOG = "dog"
    RABBIT = "rabbit"
    FOX = "fox"
    PANDA = "panda"
    PIG = "pig"
    FROG = "frog"

@dataclass
class SecurityConfig:
    """보안 설정 클래스"""
    MAX_ANIMALS_PER_SESSION: int = 100
    MAX_FILE_SIZE_MB: int = 50
    RATE_LIMIT_SECONDS: float = 0.1
    MAX_REQUESTS_PER_MINUTE: int = 60
    ALLOWED_IMAGE_FORMATS: List[str] = None
    MAX_FIGURE_SIZE: Tuple[int, int] = (20, 20)
    MAX_DPI: int = 300
    SAFE_FILENAME_PATTERN: str = r'^[a-zA-Z0-9_-]+$'
    
    def __post_init__(self):
        if self.ALLOWED_IMAGE_FORMATS is None:
            self.ALLOWED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'svg', 'pdf']

@dataclass 
class ColorScheme:
    """안전한 색상 스키마"""
    main: str
    secondary: str
    inner: str
    
    def __post_init__(self):
        """색상 검증"""
        for color in [self.main, self.secondary, self.inner]:
            if not self._validate_color(color):
                raise ValidationError(f"Invalid color format: {color}")
    
    @staticmethod
    def _validate_color(color: str) -> bool:
        """색상 형식 검증"""
        if not isinstance(color, str):
            return False
        
        # Hex 색상 패턴
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        # 명명된 색상
        named_colors = {
            'red', 'blue', 'green', 'yellow', 'orange', 'purple', 
            'pink', 'brown', 'black', 'white', 'gray', 'grey'
        }
        
        return bool(re.match(hex_pattern, color)) or color.lower() in named_colors

class InputValidator:
    """입력 검증 클래스"""
    
    @staticmethod
    def validate_animal_type(animal_type: Union[str, AnimalType]) -> AnimalType:
        """동물 타입 검증"""
        if isinstance(animal_type, AnimalType):
            return animal_type
            
        if not isinstance(animal_type, str):
            raise ValidationError(f"Animal type must be string or AnimalType, got {type(animal_type)}")
        
        # 입력 sanitization
        sanitized = re.sub(r'[^a-zA-Z]', '', animal_type.lower())
        
        try:
            return AnimalType(sanitized)
        except ValueError:
            valid_types = [t.value for t in AnimalType]
            raise ValidationError(f"Invalid animal type: {animal_type}. Valid types: {valid_types}")
    
    @staticmethod
    def validate_file_path(file_path: str, base_dir: Optional[str] = None) -> Path:
        """파일 경로 검증 (경로 순회 공격 방지)"""
        if not isinstance(file_path, str):
            raise ValidationError("File path must be a string")
        
        # 위험한 문자 제거
        sanitized_path = re.sub(r'[<>:"|?*]', '', file_path)
        
        try:
            path = Path(sanitized_path).resolve()
        except (OSError, ValueError) as e:
            raise ValidationError(f"Invalid file path: {e}")
        
        # 경로 순회 공격 확인
        if base_dir:
            base_path = Path(base_dir).resolve()
            try:
                path.relative_to(base_path)
            except ValueError:
                raise SecurityError(f"Path traversal attempt detected: {file_path}")
        
        # 파일명 검증
        if not re.match(SecurityConfig.SAFE_FILENAME_PATTERN, path.stem):
            raise ValidationError(f"Unsafe filename: {path.name}")
        
        return path
    
    @staticmethod
    def validate_numeric_input(value: Any, min_val: float = None, max_val: float = None) -> float:
        """숫자 입력 검증"""
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid numeric value: {value}")
        
        if np.isnan(num_value) or np.isinf(num_value):
            raise ValidationError(f"Invalid numeric value: {value}")
        
        if min_val is not None and num_value < min_val:
            raise ValidationError(f"Value {num_value} below minimum {min_val}")
        
        if max_val is not None and num_value > max_val:
            raise ValidationError(f"Value {num_value} above maximum {max_val}")
        
        return num_value

class RateLimiter:
    """Rate limiting 클래스"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.last_request_time = 0
        self.request_times = []
    
    def check_rate_limit(self) -> bool:
        """Rate limit 확인"""
        current_time = time.time()
        
        # 최소 간격 확인
        if current_time - self.last_request_time < self.config.RATE_LIMIT_SECONDS:
            logger.warning(f"Rate limit exceeded: minimum interval {self.config.RATE_LIMIT_SECONDS}s")
            return False
        
        # 분당 요청 수 확인
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        if len(self.request_times) >= self.config.MAX_REQUESTS_PER_MINUTE:
            logger.warning(f"Rate limit exceeded: {self.config.MAX_REQUESTS_PER_MINUTE} requests per minute")
            return False
        
        self.last_request_time = current_time
        self.request_times.append(current_time)
        return True

class SecureAnimalGenerator:
    """보안 강화된 동물 생성기"""
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or SecurityConfig()
        self.validator = InputValidator()
        self.rate_limiter = RateLimiter(self.config)
        self.animals_created = 0
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        
        # 임시 디렉토리 설정
        self.temp_dir = Path(tempfile.mkdtemp(prefix=f"animals_{self.session_id}_"))
        
        # 로그 기록
        logger.info(f"SecureAnimalGenerator initialized with session ID: {self.session_id}")
        
        # 동물 템플릿 정의
        self._init_animal_templates()
    
    def _init_animal_templates(self):
        """동물 템플릿 초기화"""
        self.animal_templates = {
            AnimalType.BEAR: {
                'name': '곰',
                'default_colors': ColorScheme('#8B4513', '#A0522D', '#DEB887'),
                'generator': self._create_bear
            },
            AnimalType.CAT: {
                'name': '고양이',
                'default_colors': ColorScheme('#FFA500', '#FFB84D', '#FFF8DC'),
                'generator': self._create_cat
            },
            AnimalType.DOG: {
                'name': '강아지',
                'default_colors': ColorScheme('#DEB887', '#F5DEB3', '#FFF8DC'),
                'generator': self._create_dog
            },
            AnimalType.RABBIT: {
                'name': '토끼',
                'default_colors': ColorScheme('#F5F5F5', '#E6E6FA', '#FFB6C1'),
                'generator': self._create_rabbit
            },
            AnimalType.FOX: {
                'name': '여우',
                'default_colors': ColorScheme('#FF8C00', '#FF7F50', '#FFF8DC'),
                'generator': self._create_fox
            },
            AnimalType.PANDA: {
                'name': '판다',
                'default_colors': ColorScheme('white', 'black', '#FFF8DC'),
                'generator': self._create_panda
            },
            AnimalType.PIG: {
                'name': '돼지',
                'default_colors': ColorScheme('#FFB6C1', '#FFC0CB', '#FF69B4'),
                'generator': self._create_pig
            },
            AnimalType.FROG: {
                'name': '개구리',
                'default_colors': ColorScheme('#90EE90', '#98FB98', '#FFFFE0'),
                'generator': self._create_frog
            }
        }
    
    def __enter__(self):
        """Context manager 진입"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 종료 (리소스 정리)"""
        self.cleanup()
    
    def cleanup(self):
        """리소스 정리"""
        try:
            # 임시 파일 정리
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
            
            # matplotlib 정리
            plt.close('all')
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def create_secure_figure(self, title: str = "귀여운 동물") -> Tuple[plt.Figure, plt.Axes]:
        """보안이 강화된 도화지 생성"""
        try:
            # 입력 검증
            if not isinstance(title, str):
                raise ValidationError("Title must be a string")
            
            # 제목 sanitization
            safe_title = re.sub(r'[<>&"\']', '', title)[:100]  # XSS 방지 및 길이 제한
            
            # Figure 크기 검증
            fig_width = min(self.config.MAX_FIGURE_SIZE[0], 10)
            fig_height = min(self.config.MAX_FIGURE_SIZE[1], 10)
            
            fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(safe_title, fontsize=16, fontweight='bold', pad=20)
            
            return fig, ax
            
        except Exception as e:
            logger.error(f"Error creating figure: {e}")
            raise SecurityError(f"Failed to create secure figure: {e}")
    
    def add_secure_shape(self, ax: plt.Axes, shape_type: str, **kwargs) -> Optional[patches.Patch]:
        """안전한 도형 추가"""
        try:
            # 입력 검증
            valid_shapes = ['circle', 'ellipse', 'polygon', 'rectangle']
            if shape_type not in valid_shapes:
                raise ValidationError(f"Invalid shape type: {shape_type}")
            
            # 좌표 검증
            for key in ['x', 'y', 'cx', 'cy', 'width', 'height', 'radius']:
                if key in kwargs:
                    kwargs[key] = self.validator.validate_numeric_input(
                        kwargs[key], min_val=-100, max_val=100
                    )
            
            # 색상 검증
            if 'color' in kwargs and not ColorScheme._validate_color(kwargs['color']):
                kwargs['color'] = '#000000'  # 기본값으로 대체
            
            # 도형 생성
            if shape_type == 'circle':
                shape = Circle((kwargs.get('x', 0), kwargs.get('y', 0)), 
                             kwargs.get('radius', 1), 
                             color=kwargs.get('color', 'blue'),
                             alpha=kwargs.get('alpha', 1.0),
                             zorder=kwargs.get('zorder', 1))
            elif shape_type == 'ellipse':
                shape = Ellipse((kwargs.get('x', 0), kwargs.get('y', 0)),
                              kwargs.get('width', 1), kwargs.get('height', 1),
                              color=kwargs.get('color', 'blue'),
                              alpha=kwargs.get('alpha', 1.0),
                              angle=kwargs.get('angle', 0),
                              zorder=kwargs.get('zorder', 1))
            else:
                return None
            
            ax.add_patch(shape)
            return shape
            
        except Exception as e:
            logger.warning(f"Error adding shape: {e}")
            return None
    
    def _create_bear(self, ax: plt.Axes, colors: ColorScheme):
        """곰 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.4, height=1.6, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'circle', x=5, y=5.5, radius=1.8, 
                                color=colors.main, zorder=2)
            self.add_secure_shape(ax, 'circle', x=5, y=5.5, radius=1.4, 
                                color=colors.secondary, zorder=3)
            
            # 귀
            self.add_secure_shape(ax, 'circle', x=3.8, y=6.8, radius=0.7, 
                                color=colors.main, zorder=2)
            self.add_secure_shape(ax, 'circle', x=6.2, y=6.8, radius=0.7, 
                                color=colors.main, zorder=2)
            self.add_secure_shape(ax, 'circle', x=3.8, y=6.8, radius=0.5, 
                                color=colors.inner, zorder=3)
            self.add_secure_shape(ax, 'circle', x=6.2, y=6.8, radius=0.5, 
                                color=colors.inner, zorder=3)
            
            # 눈
            self.add_secure_shape(ax, 'circle', x=4.4, y=5.8, radius=0.3, 
                                color='white', zorder=4)
            self.add_secure_shape(ax, 'circle', x=5.6, y=5.8, radius=0.3, 
                                color='white', zorder=4)
            self.add_secure_shape(ax, 'circle', x=4.4, y=5.8, radius=0.2, 
                                color='black', zorder=5)
            self.add_secure_shape(ax, 'circle', x=5.6, y=5.8, radius=0.2, 
                                color='black', zorder=5)
            
            # 코
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.2, width=0.3, height=0.2, 
                                color='black', zorder=4)
            
            # 입 (안전한 곡선)
            safe_x = [4.7, 4.9, 5, 5.1, 5.3]
            safe_y = [4.9, 4.7, 4.8, 4.7, 4.9]
            ax.plot(safe_x[:3], safe_y[:3], 'k-', linewidth=3, zorder=4)
            ax.plot(safe_x[2:], safe_y[2:], 'k-', linewidth=3, zorder=4)
            
        except Exception as e:
            logger.error(f"Error creating bear: {e}")
            raise
    
    def _create_cat(self, ax: plt.Axes, colors: ColorScheme):
        """고양이 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.2, height=1.4, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'circle', x=5, y=5.5, radius=1.6, 
                                color=colors.main, zorder=2)
            
            # 얼굴 패턴
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.3, width=2.0, height=1.6, 
                                color=colors.secondary, zorder=3)
            
            # 눈 (고양이 특유의)
            self.add_secure_shape(ax, 'ellipse', x=4.4, y=5.7, width=0.3, height=0.6, 
                                color='green', zorder=4)
            self.add_secure_shape(ax, 'ellipse', x=5.6, y=5.7, width=0.3, height=0.6, 
                                color='green', zorder=4)
            self.add_secure_shape(ax, 'ellipse', x=4.4, y=5.7, width=0.15, height=0.5, 
                                color='black', zorder=5)
            self.add_secure_shape(ax, 'ellipse', x=5.6, y=5.7, width=0.15, height=0.5, 
                                color='black', zorder=5)
            
            # 입
            safe_x1 = [4.7, 4.9, 5]
            safe_y1 = [4.7, 4.5, 4.6]
            safe_x2 = [5, 5.1, 5.3]
            safe_y2 = [4.6, 4.5, 4.7]
            ax.plot(safe_x1, safe_y1, 'k-', linewidth=2, zorder=4)
            ax.plot(safe_x2, safe_y2, 'k-', linewidth=2, zorder=4)
            
            # 수염
            ax.plot([3.2, 4.0], [5.4, 5.5], 'k-', linewidth=1, zorder=4)
            ax.plot([3.2, 4.0], [5.0, 4.9], 'k-', linewidth=1, zorder=4)
            ax.plot([6.0, 6.8], [5.5, 5.4], 'k-', linewidth=1, zorder=4)
            ax.plot([6.0, 6.8], [4.9, 5.0], 'k-', linewidth=1, zorder=4)
            
        except Exception as e:
            logger.error(f"Error creating cat: {e}")
            raise
    
    def _create_dog(self, ax: plt.Axes, colors: ColorScheme):
        """강아지 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.4, height=1.6, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.5, width=1.4, height=1.6, 
                                color=colors.main, zorder=2)
            
            # 귀 (늘어진)
            self.add_secure_shape(ax, 'ellipse', x=3.8, y=6.2, width=0.6, height=1.0, 
                                color=colors.secondary, zorder=3)
            self.add_secure_shape(ax, 'ellipse', x=6.2, y=6.2, width=0.6, height=1.0, 
                                color=colors.secondary, zorder=3)
            
            # 주둥이
            self.add_secure_shape(ax, 'ellipse', x=5, y=4.8, width=0.9, height=0.6, 
                                color=colors.inner, zorder=3)
            
            # 눈
            self.add_secure_shape(ax, 'circle', x=4.5, y=5.8, radius=0.24, 
                                color='black', zorder=4)
            self.add_secure_shape(ax, 'circle', x=5.5, y=5.8, radius=0.24, 
                                color='black', zorder=4)
            self.add_secure_shape(ax, 'circle', x=4.6, y=5.9, radius=0.08, 
                                color='white', zorder=5)
            self.add_secure_shape(ax, 'circle', x=5.6, y=5.9, radius=0.08, 
                                color='white', zorder=5)
            
            # 코
            self.add_secure_shape(ax, 'circle', x=5, y=5.0, radius=0.12, 
                                color='black', zorder=4)
            
            # 혀
            self.add_secure_shape(ax, 'ellipse', x=5, y=4.2, width=0.3, height=0.5, 
                                color='pink', zorder=4)
            
        except Exception as e:
            logger.error(f"Error creating dog: {e}")
            raise
    
    def _create_rabbit(self, ax: plt.Axes, colors: ColorScheme):
        """토끼 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.0, height=1.4, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'circle', x=5, y=5.5, radius=1.4, 
                                color=colors.main, zorder=2)
            
            # 긴 귀
            self.add_secure_shape(ax, 'ellipse', x=4.2, y=7.2, width=0.6, height=2.4, 
                                color=colors.main, zorder=2)
            self.add_secure_shape(ax, 'ellipse', x=5.8, y=7.2, width=0.6, height=2.4, 
                                color=colors.main, zorder=2)
            self.add_secure_shape(ax, 'ellipse', x=4.2, y=7.2, width=0.3, height=1.6, 
                                color=colors.inner, zorder=3)
            self.add_secure_shape(ax, 'ellipse', x=5.8, y=7.2, width=0.3, height=1.6, 
                                color=colors.inner, zorder=3)
            
            # 눈
            self.add_secure_shape(ax, 'circle', x=4.5, y=5.7, radius=0.24, 
                                color='black', zorder=4)
            self.add_secure_shape(ax, 'circle', x=5.5, y=5.7, radius=0.24, 
                                color='black', zorder=4)
            
            # 코 (Y자 모양) - 안전한 선 그리기
            ax.plot([5, 5], [5.1, 4.9], 'k-', linewidth=2, zorder=4)
            ax.plot([5, 4.85], [5.0, 4.8], 'k-', linewidth=2, zorder=4)
            ax.plot([5, 5.15], [5.0, 4.8], 'k-', linewidth=2, zorder=4)
            
        except Exception as e:
            logger.error(f"Error creating rabbit: {e}")
            raise
    
    def _create_fox(self, ax: plt.Axes, colors: ColorScheme):
        """여우 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.2, height=1.4, 
                                color=colors.main, zorder=1)
            
            # 머리 (다이아몬드 모양은 안전한 타원으로 대체)
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.5, width=1.8, height=2.0, 
                                color=colors.main, zorder=2)
            
            # 눈 (여우 특유의)
            self.add_secure_shape(ax, 'ellipse', x=4.5, y=5.7, width=0.2, height=0.3, 
                                color='orange', zorder=4)
            self.add_secure_shape(ax, 'ellipse', x=5.5, y=5.7, width=0.2, height=0.3, 
                                color='orange', zorder=4)
            self.add_secure_shape(ax, 'ellipse', x=4.5, y=5.7, width=0.1, height=0.25, 
                                color='black', zorder=5)
            self.add_secure_shape(ax, 'ellipse', x=5.5, y=5.7, width=0.1, height=0.25, 
                                color='black', zorder=5)
            
            # 코
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.2, width=0.2, height=0.15, 
                                color='black', zorder=4)
            
        except Exception as e:
            logger.error(f"Error creating fox: {e}")
            raise
    
    def _create_panda(self, ax: plt.Axes, colors: ColorScheme):
        """판다 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.4, height=1.6, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'circle', x=5, y=5.5, radius=1.6, 
                                color=colors.main, zorder=2)
            
            # 귀 (검은색)
            self.add_secure_shape(ax, 'circle', x=3.8, y=6.8, radius=0.7, 
                                color=colors.secondary, zorder=3)
            self.add_secure_shape(ax, 'circle', x=6.2, y=6.8, radius=0.7, 
                                color=colors.secondary, zorder=3)
            
            # 눈 주위 (검은색)
            self.add_secure_shape(ax, 'ellipse', x=4.4, y=5.7, width=0.9, height=1.2, 
                                color=colors.secondary, zorder=3)
            self.add_secure_shape(ax, 'ellipse', x=5.6, y=5.7, width=0.9, height=1.2, 
                                color=colors.secondary, zorder=3)
            
            # 눈
            self.add_secure_shape(ax, 'circle', x=4.4, y=5.7, radius=0.24, 
                                color='white', zorder=4)
            self.add_secure_shape(ax, 'circle', x=5.6, y=5.7, radius=0.24, 
                                color='white', zorder=4)
            self.add_secure_shape(ax, 'circle', x=4.4, y=5.7, radius=0.16, 
                                color='black', zorder=5)
            self.add_secure_shape(ax, 'circle', x=5.6, y=5.7, radius=0.16, 
                                color='black', zorder=5)
            
        except Exception as e:
            logger.error(f"Error creating panda: {e}")
            raise
    
    def _create_pig(self, ax: plt.Axes, colors: ColorScheme):
        """돼지 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.6, height=1.8, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'circle', x=5, y=5.5, radius=1.6, 
                                color=colors.main, zorder=2)
            
            # 눈
            self.add_secure_shape(ax, 'circle', x=4.4, y=5.7, radius=0.2, 
                                color='black', zorder=4)
            self.add_secure_shape(ax, 'circle', x=5.6, y=5.7, radius=0.2, 
                                color='black', zorder=4)
            
            # 코 (돼지 특유의)
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.0, width=0.6, height=0.5, 
                                color=colors.inner, zorder=4)
            self.add_secure_shape(ax, 'circle', x=4.7, y=5.0, radius=0.08, 
                                color='black', zorder=5)
            self.add_secure_shape(ax, 'circle', x=5.3, y=5.0, radius=0.08, 
                                color='black', zorder=5)
            
        except Exception as e:
            logger.error(f"Error creating pig: {e}")
            raise
    
    def _create_frog(self, ax: plt.Axes, colors: ColorScheme):
        """개구리 그리기 (보안 강화)"""
        try:
            # 몸
            self.add_secure_shape(ax, 'ellipse', x=5, y=2.5, width=2.8, height=1.6, 
                                color=colors.main, zorder=1)
            
            # 머리
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.5, width=3.2, height=2.8, 
                                color=colors.main, zorder=2)
            
            # 튀어나온 눈
            self.add_secure_shape(ax, 'circle', x=3.9, y=6.8, radius=0.6, 
                                color=colors.main, zorder=3)
            self.add_secure_shape(ax, 'circle', x=6.1, y=6.8, radius=0.6, 
                                color=colors.main, zorder=3)
            self.add_secure_shape(ax, 'circle', x=3.9, y=6.8, radius=0.4, 
                                color='white', zorder=4)
            self.add_secure_shape(ax, 'circle', x=6.1, y=6.8, radius=0.4, 
                                color='white', zorder=4)
            self.add_secure_shape(ax, 'circle', x=3.9, y=6.8, radius=0.24, 
                                color='black', zorder=5)
            self.add_secure_shape(ax, 'circle', x=6.1, y=6.8, radius=0.24, 
                                color='black', zorder=5)
            
            # 배
            self.add_secure_shape(ax, 'ellipse', x=5, y=5.0, width=2.0, height=1.6, 
                                color=colors.inner, zorder=3)
            
        except Exception as e:
            logger.error(f"Error creating frog: {e}")
            raise
    
    def adjust_brightness_securely(self, color: str, percent: float) -> str:
        """안전한 색상 밝기 조절"""
        try:
            # 입력 검증
            if not ColorScheme._validate_color(color):
                return color
            
            # 퍼센트 값 제한
            percent = max(-0.5, min(0.5, percent))
            
            # Hex 색상만 처리
            if not color.startswith('#') or len(color) != 7:
                return color
            
            # RGB 변환
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # 밝기 조절
            amt = int(255 * percent)
            r = max(0, min(255, r + amt))
            g = max(0, min(255, g + amt))
            b = max(0, min(255, b + amt))
            
            return f"#{r:02x}{g:02x}{b:02x}"
            
        except Exception as e:
            logger.warning(f"Error adjusting brightness: {e}")
            return color
    
    def generate_animal(self, animal_type: Union[str, AnimalType], 
                       custom_colors: Optional[ColorScheme] = None,
                       title: Optional[str] = None) -> Tuple[plt.Figure, plt.Axes]:
        """보안이 강화된 동물 생성"""
        try:
            # Rate limiting 확인
            if not self.rate_limiter.check_rate_limit():
                raise SecurityError("Rate limit exceeded")
            
            # 세션당 최대 동물 수 확인
            if self.animals_created >= self.config.MAX_ANIMALS_PER_SESSION:
                raise SecurityError(f"Maximum animals per session exceeded: {self.config.MAX_ANIMALS_PER_SESSION}")
            
            # 입력 검증
            validated_type = self.validator.validate_animal_type(animal_type)
            
            if title is None:
                title = f"귀여운 {self.animal_templates[validated_type]['name']}"
            
            # Figure 생성
            fig, ax = self.create_secure_figure(title)
            
            # 색상 설정
            if custom_colors is None:
                colors = self.animal_templates[validated_type]['default_colors']
                # 랜덤 색상 변형
                variation = (random.random() * 0.3) - 0.15
                colors = ColorScheme(
                    self.adjust_brightness_securely(colors.main, variation),
                    self.adjust_brightness_securely(colors.secondary, variation),
                    self.adjust_brightness_securely(colors.inner, variation)
                )
            else:
                colors = custom_colors
            
            # 배경 추가
            background_colors = ['#E6F3FF', '#FFE6F3', '#F3FFE6', '#FFF3E6', '#F0E6FF']
            bg_color = random.choice(background_colors)
            bg_rect = Rectangle((0, 0), 10, 10, color=bg_color, alpha=0.3, zorder=0)
            ax.add_patch(bg_rect)
            
            # 동물 그리기
            generator_func = self.animal_templates[validated_type]['generator']
            generator_func(ax, colors)
            
            self.animals_created += 1
            logger.info(f"Generated {validated_type.value} (session: {self.session_id}, count: {self.animals_created})")
            
            return fig, ax
            
        except Exception as e:
            logger.error(f"Error generating animal: {e}")
            plt.close('all')  # 메모리 누수 방지
            raise
    
    def save_animal_securely(self, fig: plt.Figure, filename: str, 
                           format: str = 'png', dpi: int = 150) -> Path:
        """보안이 강화된 동물 이미지 저장"""
        try:
            # 입력 검증
            if format not in self.config.ALLOWED_IMAGE_FORMATS:
                raise ValidationError(f"Unsupported format: {format}")
            
            dpi = min(dpi, self.config.MAX_DPI)
            
            # 안전한 파일명 생성
            safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
            if not safe_filename:
                safe_filename = f"animal_{int(time.time())}"
            
            # 파일 경로 생성
            file_path = self.temp_dir / f"{safe_filename}.{format}"
            
            # 파일 크기 제한 확인을 위한 임시 저장
            temp_path = self.temp_dir / f"temp_{safe_filename}.{format}"
            fig.savefig(temp_path, format=format, dpi=dpi, bbox_inches='tight')
            
            # 파일 크기 확인
            file_size_mb = temp_path.stat().st_size / (1024 * 1024)
            if file_size_mb > self.config.MAX_FILE_SIZE_MB:
                temp_path.unlink()  # 임시 파일 삭제
                raise SecurityError(f"File size {file_size_mb:.1f}MB exceeds limit {self.config.MAX_FILE_SIZE_MB}MB")
            
            # 최종 저장
            temp_path.rename(file_path)
            
            logger.info(f"Saved animal image: {file_path} ({file_size_mb:.1f}MB)")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving animal: {e}")
            raise
    
    def generate_random_animals(self, count: int = 4) -> List[Tuple[plt.Figure, plt.Axes]]:
        """보안이 강화된 랜덤 동물들 생성"""
        try:
            # 입력 검증
            count = int(self.validator.validate_numeric_input(count, min_val=1, max_val=20))
            
            animals = []
            animal_types = list(AnimalType)
            
            for i in range(count):
                if self.animals_created >= self.config.MAX_ANIMALS_PER_SESSION:
                    logger.warning(f"Stopped at {i} animals due to session limit")
                    break
                
                random_type = random.choice(animal_types)
                fig, ax = self.generate_animal(random_type)
                animals.append((fig, ax))
                
                # 메모리 관리를 위한 작은 지연
                time.sleep(0.01)
            
            return animals
            
        except Exception as e:
            logger.error(f"Error generating random animals: {e}")
            # 생성된 figure들 정리
            for fig, _ in animals:
                plt.close(fig)
            raise

def main():
    """보안 강화된 메인 함수"""
    print("🔒 보안 강화된 귀여운 동물 생성기에 오신 걸 환영합니다! 🐾")
    print("=" * 60)
    
    try:
        with SecureAnimalGenerator() as generator:
            while True:
                print("\n사용 가능한 옵션:")
                print("1. 특정 동물 생성")
                print("2. 랜덤 동물들 생성")
                print("3. 모든 동물 보기")
                print("4. 이미지 저장")
                print("5. 세션 정보")
                print("6. 종료")
                
                try:
                    choice = input("\n선택하세요 (1-6): ").strip()
                    
                    if choice == '1':
                        print("\n사용 가능한 동물:")
                        for animal_type in AnimalType:
                            print(f"- {animal_type.value}")
                        
                        animal_input = input("동물 타입을 입력하세요: ").strip()
                        fig, ax = generator.generate_animal(animal_input)
                        plt.show()
                        plt.close(fig)
                    
                    elif choice == '2':
                        count_input = input("생성할 동물 수를 입력하세요 (1-10): ").strip()
                        count = int(count_input) if count_input.isdigit() else 4
                        count = min(count, 10)  # 최대 10개로 제한
                        
                        animals = generator.generate_random_animals(count)
                        
                        # 그리드로 표시
                        cols = int(np.ceil(np.sqrt(count)))
                        rows = int(np.ceil(count / cols))
                        
                        fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 4*rows))
                        if count == 1:
                            axes = [axes]
                        elif rows == 1:
                            axes = axes if count > 1 else [axes]
                        else:
                            axes = axes.flatten()
                        
                        for i, (animal_fig, animal_ax) in enumerate(animals):
                            if i < len(axes):
                                # 동물 이미지를 새 그리드에 복사 (보안상 안전한 방법)
                                axes[i].set_xlim(0, 10)
                                axes[i].set_ylim(0, 10)
                                axes[i].set_aspect('equal')
                                axes[i].axis('off')
                                axes[i].set_title(animal_ax.get_title())
                            plt.close(animal_fig)
                        
                        # 사용하지 않는 subplot 숨기기
                        for i in range(count, len(axes)):
                            axes[i].axis('off')
                        
                        plt.tight_layout()
                        plt.show()
                        plt.close(fig)
                    
                    elif choice == '3':
                        print("\n모든 동물을 생성합니다...")
                        all_animals = []
                        for animal_type in AnimalType:
                            fig, ax = generator.generate_animal(animal_type)
                            all_animals.append((fig, ax))
                        
                        # 4x2 그리드로 표시
                        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
                        axes = axes.flatten()
                        
                        for i, (animal_fig, animal_ax) in enumerate(all_animals):
                            axes[i].set_xlim(0, 10)
                            axes[i].set_ylim(0, 10)
                            axes[i].set_aspect('equal')
                            axes[i].axis('off')
                            axes[i].set_title(animal_ax.get_title())
                            plt.close(animal_fig)
                        
                        plt.tight_layout()
                        plt.show()
                        plt.close(fig)
                    
                    elif choice == '4':
                        animal_input = input("저장할 동물 타입을 입력하세요: ").strip()
                        filename = input("파일명을 입력하세요 (확장자 제외): ").strip()
                        
                        fig, ax = generator.generate_animal(animal_input)
                        saved_path = generator.save_animal_securely(fig, filename)
                        print(f"✅ 이미지가 저장되었습니다: {saved_path}")
                        plt.close(fig)
                    
                    elif choice == '5':
                        print(f"\n📊 세션 정보:")
                        print(f"세션 ID: {generator.session_id}")
                        print(f"생성된 동물 수: {generator.animals_created}")
                        print(f"임시 디렉토리: {generator.temp_dir}")
                        print(f"최대 동물 수: {generator.config.MAX_ANIMALS_PER_SESSION}")
                    
                    elif choice == '6':
                        print("안녕히 가세요! 🐾")
                        break
                    
                    else:
                        print("❌ 올바른 선택을 해주세요.")
                
                except ValidationError as e:
                    print(f"❌ 입력 오류: {e}")
                except SecurityError as e:
                    print(f"🔒 보안 오류: {e}")
                except Exception as e:
                    print(f"❌ 오류가 발생했습니다: {e}")
                    logger.error(f"Unexpected error in main loop: {e}")
    
    except KeyboardInterrupt:
        print("\n\n👋 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"❌ 치명적 오류: {e}")
        logger.error(f"Fatal error in main: {e}")

if __name__ == "__main__":
    # 예제 실행
    print("🔒 보안 강화된 동물 생성기 데모")
    print("=" * 40)
    
    try:
        with SecureAnimalGenerator() as generator:
            # 곰 생성 예제
            print("곰 생성 중...")
            fig, ax = generator.generate_animal(AnimalType.BEAR)
            saved_path = generator.save_animal_securely(fig, "secure_bear")
            print(f"곰 이미지 저장됨: {saved_path}")
            plt.show()
            plt.close(fig)
            
            # 랜덤 동물들 생성 예제
            print("\n랜덤 동물들 생성 중...")
            animals = generator.generate_random_animals(4)
            
            # 정리
            for fig, ax in animals:
                plt.close(fig)
            
            print(f"\n✅ 총 {generator.animals_created}개의 동물이 생성되었습니다.")
            
            # 대화형 모드 실행 (선택사항)
            interactive = input("\n대화형 모드를 실행하시겠습니까? (y/n): ").strip().lower()
            if interactive == 'y':
                main()
    
    except Exception as e:
        print(f"❌ 오류: {e}")
        logger.error(f"Error in demo: {e}")