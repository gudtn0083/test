import streamlit as st
import torch
from PIL import Image
import io
import base64
import hashlib
import secrets
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from cute_animal_generator import CuteAnimalGenerator, quick_generate, SecurityError, InputValidator
import time

# 보안 설정
st.set_page_config(
    page_title="🐾 귀여운 동물 AI 생성기",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebAppSecurity:
    """웹앱 보안 관리 클래스"""
    
    # 최대 요청 횟수 (시간당)
    MAX_REQUESTS_PER_HOUR = 50
    
    # 최대 이미지 생성 횟수 (일일)
    MAX_IMAGES_PER_DAY = 100
    
    # 세션 타임아웃 (분)
    SESSION_TIMEOUT = 30
    
    @staticmethod
    def init_session():
        """세션 초기화 및 보안 설정"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = secrets.token_hex(16)
            st.session_state.session_start = datetime.now()
            st.session_state.request_count = 0
            st.session_state.image_count = 0
            st.session_state.last_request = datetime.now()
        
        # 세션 타임아웃 체크
        if datetime.now() - st.session_state.last_request > timedelta(minutes=WebAppSecurity.SESSION_TIMEOUT):
            st.session_state.clear()
            st.rerun()
    
    @staticmethod
    def check_rate_limit() -> bool:
        """요청 횟수 제한 체크"""
        WebAppSecurity.init_session()
        
        # 시간당 요청 제한
        if st.session_state.request_count >= WebAppSecurity.MAX_REQUESTS_PER_HOUR:
            return False
        
        # 일일 이미지 생성 제한
        if st.session_state.image_count >= WebAppSecurity.MAX_IMAGES_PER_DAY:
            return False
        
        return True
    
    @staticmethod
    def log_request(request_type: str):
        """요청 로깅"""
        st.session_state.request_count += 1
        st.session_state.last_request = datetime.now()
        
        if request_type == "image_generation":
            st.session_state.image_count += 1
        
        logger.info(f"Request: {request_type}, Session: {st.session_state.session_id[:8]}")
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """사용자 입력 정화"""
        try:
            return InputValidator.validate_prompt(user_input)
        except SecurityError:
            return ""
    
    @staticmethod
    def validate_file_upload(uploaded_file) -> bool:
        """파일 업로드 검증"""
        if not uploaded_file:
            return False
        
        # 파일 크기 체크
        if uploaded_file.size > InputValidator.MAX_FILE_SIZE:
            return False
        
        # 파일 확장자 체크
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in InputValidator.ALLOWED_EXTENSIONS:
            return False
        
        return True

@st.cache_resource
def load_generator():
    """AI 생성기 로드 (캐시됨, 보안 강화)"""
    try:
        return CuteAnimalGenerator()
    except Exception as e:
        logger.error(f"Failed to load generator: {e}")
        st.error("AI 모델 로딩에 실패했습니다. 관리자에게 문의하세요.")
        return None

def secure_image_to_base64(image: Image.Image) -> str:
    """이미지를 안전하게 base64로 변환"""
    try:
        if not isinstance(image, Image.Image):
            raise SecurityError("Invalid image type")
        
        # 이미지 크기 제한
        if image.size[0] > InputValidator.MAX_IMAGE_SIZE or image.size[1] > InputValidator.MAX_IMAGE_SIZE:
            image = image.resize((min(image.size[0], InputValidator.MAX_IMAGE_SIZE), 
                                min(image.size[1], InputValidator.MAX_IMAGE_SIZE)), 
                               Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        # Base64 문자열 길이 제한
        if len(img_str) > 10 * 1024 * 1024:  # 10MB
            raise SecurityError("Image too large after encoding")
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        logger.error(f"Image encoding failed: {e}")
        return ""

def main():
    # 보안 초기화
    WebAppSecurity.init_session()
    
    # Rate limiting 체크
    if not WebAppSecurity.check_rate_limit():
        st.error("🚫 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
        st.stop()
    
    # 헤더 (XSS 방지를 위해 사용자 입력 없음)
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem;">
        <h1>🐾 귀여운 동물 AI 이미지 생성기 🐾</h1>
        <p>AI가 만드는 세상에서 가장 귀여운 동물 친구들을 만나보세요!</p>
    </div>
    """, unsafe_allow_html=True)

    # 보안 CSS (inline styles만 사용)
    st.markdown("""
    <style>
        .stButton > button {
            background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: bold;
        }
        .stSelectbox > div > div {
            background-color: #fff5f5;
        }
        .stTextArea > div > div > textarea {
            background-color: #fff5f5;
        }
    </style>
    """, unsafe_allow_html=True)

    # 사이드바 설정 (보안 강화)
    st.sidebar.markdown("## 🎨 생성 설정")
    
    # 동물 선택 (화이트리스트 방식)
    safe_animal_types = [
        "랜덤 선택", "강아지", "고양이", "아기 판다", "아기 여우", "아기 토끼",
        "아기 곰", "아기 코끼리", "아기 펭귄", "아기 부엉이", "아기 사슴",
        "아기 물개", "아기 고슴도치", "아기 라쿤", "아기 코알라", "햄스터"
    ]
    
    animal_map = {
        "랜덤 선택": None,
        "강아지": "puppy",
        "고양이": "kitten", 
        "아기 판다": "baby panda",
        "아기 여우": "baby fox",
        "아기 토끼": "baby rabbit",
        "아기 곰": "baby bear",
        "아기 코끼리": "baby elephant",
        "아기 펭귄": "baby penguin",
        "아기 부엉이": "baby owl",
        "아기 사슴": "baby deer",
        "아기 물개": "baby seal",
        "아기 고슴도치": "baby hedgehog",
        "아기 라쿤": "baby raccoon",
        "아기 코알라": "baby koala",
        "햄스터": "hamster"
    }
    
    selected_animal = st.sidebar.selectbox("🐾 동물 선택", safe_animal_types)
    
    # 스타일 설정 (화이트리스트 방식)
    safe_style_options = [
        "자동 선택", "카와이 스타일", "치비 스타일", "만화 스타일", 
        "애니메이션 스타일", "픽사 스타일", "디즈니 스타일", "지브리 스타일"
    ]
    
    selected_style = st.sidebar.selectbox("🎨 스타일 선택", safe_style_options)
    
    # 고급 설정 (안전한 범위로 제한)
    st.sidebar.markdown("### ⚙️ 고급 설정")
    
    image_size = st.sidebar.selectbox(
        "📐 이미지 크기",
        ["512x512 (기본)", "768x768 (고화질)", "1024x1024 (최고화질)"]
    )
    
    size_map = {
        "512x512 (기본)": (512, 512),
        "768x768 (고화질)": (768, 768), 
        "1024x1024 (최고화질)": (1024, 1024)
    }
    
    width, height = size_map[image_size]
    
    # 안전한 범위로 제한
    num_steps = st.sidebar.slider("🔄 생성 품질", min_value=10, max_value=50, value=20)
    guidance_scale = st.sidebar.slider("🎯 창의성 조절", min_value=5.0, max_value=15.0, value=7.5, step=0.5)
    
    # 커스텀 프롬프트 (보안 강화)
    st.sidebar.markdown("### ✍️ 커스텀 프롬프트")
    raw_custom_prompt = st.sidebar.text_area(
        "원하는 상세 설명을 입력하세요 (최대 1000자)",
        placeholder="예: 분홍색 리본을 한 하얀 강아지가 꽃밭에서 뛰어놀고 있어요",
        max_chars=1000
    )
    
    # 입력 정화
    custom_prompt = WebAppSecurity.sanitize_input(raw_custom_prompt) if raw_custom_prompt else ""
    
    # 위험한 내용 감지시 경고
    if raw_custom_prompt and not custom_prompt:
        st.sidebar.warning("⚠️ 입력에 부적절한 내용이 포함되어 있습니다.")
    
    # 메인 컨텐츠
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 이미지 생성")
        
        # 생성 버튼 (보안 강화)
        if st.button("🎨 귀여운 동물 생성하기!", key="generate_single"):
            WebAppSecurity.log_request("image_generation")
            
            try:
                if 'generator' not in st.session_state:
                    with st.spinner("AI 모델을 로딩 중입니다... (최초 실행시 시간이 걸릴 수 있습니다)"):
                        generator = load_generator()
                        if generator is None:
                            st.error("AI 모델 로딩에 실패했습니다.")
                            st.stop()
                        st.session_state.generator = generator
                
                with st.spinner("귀여운 동물을 생성 중입니다... 🎨"):
                    generator = st.session_state.generator
                    
                    # 안전한 파라미터로 이미지 생성
                    if custom_prompt:
                        prompt = custom_prompt
                        if selected_style != "자동 선택":
                            style_suffix = selected_style.replace(" 스타일", " style")
                            prompt += f", {style_suffix}"
                        images = generator.generate_image(
                            prompt=prompt,
                            width=width,
                            height=height,
                            num_inference_steps=num_steps,
                            guidance_scale=guidance_scale
                        )
                    else:
                        animal = animal_map[selected_animal]
                        images = generator.generate_image(
                            animal=animal,
                            width=width,
                            height=height,
                            num_inference_steps=num_steps,
                            guidance_scale=guidance_scale
                        )
                    
                    # 후처리
                    enhanced_image = generator.enhance_cuteness(images[0])
                    final_image = generator.add_cute_effects(enhanced_image)
                    
                    # 세션 상태에 안전하게 저장
                    st.session_state.generated_image = final_image
                    st.session_state.generation_time = time.time()
                    
                    st.success("✨ 귀여운 동물이 생성되었습니다!")
                    
            except SecurityError as e:
                logger.warning(f"Security error: {e}")
                st.error("🚨 보안 오류가 발생했습니다. 입력을 확인해주세요.")
            except Exception as e:
                logger.error(f"Generation error: {e}")
                st.error("생성 중 오류가 발생했습니다. 다시 시도해주세요.")
        
        # 배치 생성 (보안 강화)
        st.markdown("### 🎪 배치 생성")
        batch_count = st.slider("생성할 이미지 수", min_value=2, max_value=4, value=3)  # 최대값 제한
        
        if st.button("🎪 여러 동물 한번에 생성하기!", key="generate_batch"):
            WebAppSecurity.log_request("batch_generation")
            
            # 배치 생성 제한 확인
            if st.session_state.image_count + batch_count > WebAppSecurity.MAX_IMAGES_PER_DAY:
                st.error("🚫 일일 이미지 생성 한도를 초과합니다.")
                st.stop()
            
            try:
                if 'generator' not in st.session_state:
                    with st.spinner("AI 모델을 로딩 중입니다..."):
                        generator = load_generator()
                        if generator is None:
                            st.error("AI 모델 로딩에 실패했습니다.")
                            st.stop()
                        st.session_state.generator = generator
                
                with st.spinner(f"{batch_count}마리의 귀여운 동물들을 생성 중입니다..."):
                    generator = st.session_state.generator
                    
                    # 배치 생성
                    batch_images = []
                    for i in range(batch_count):
                        try:
                            animal = animal_map[selected_animal] if selected_animal != "랜덤 선택" else None
                            images = generator.generate_image(
                                animal=animal,
                                width=width//2,  # 배치일 때는 작은 크기
                                height=height//2,
                                num_inference_steps=num_steps,
                                guidance_scale=guidance_scale
                            )
                            enhanced = generator.enhance_cuteness(images[0])
                            final = generator.add_cute_effects(enhanced)
                            batch_images.append(final)
                            
                            # 이미지 카운트 증가
                            st.session_state.image_count += 1
                            
                        except Exception as e:
                            logger.error(f"Batch image {i+1} failed: {e}")
                            continue
                    
                    if batch_images:
                        st.session_state.batch_images = batch_images
                        st.success(f"✨ {len(batch_images)}마리의 귀여운 동물들이 생성되었습니다!")
                    else:
                        st.error("배치 생성에 실패했습니다.")
                        
            except SecurityError as e:
                logger.warning(f"Security error in batch: {e}")
                st.error("🚨 보안 오류가 발생했습니다.")
            except Exception as e:
                logger.error(f"Batch generation error: {e}")
                st.error("배치 생성 중 오류가 발생했습니다.")
    
    with col2:
        st.markdown("### 🖼️ 생성된 이미지")
        
        # 단일 이미지 표시 (보안 강화)
        if 'generated_image' in st.session_state:
            try:
                st.image(
                    st.session_state.generated_image,
                    caption="생성된 귀여운 동물 🐾",
                    use_column_width=True
                )
                
                # 안전한 다운로드 버튼
                buffer = io.BytesIO()
                st.session_state.generated_image.save(buffer, format="PNG", optimize=True)
                
                # 파일명 생성 (안전한 문자만 사용)
                timestamp = int(st.session_state.generation_time)
                safe_filename = f"cute_animal_{timestamp}.png"
                
                st.download_button(
                    label="💾 이미지 다운로드",
                    data=buffer.getvalue(),
                    file_name=safe_filename,
                    mime="image/png"
                )
            except Exception as e:
                logger.error(f"Image display error: {e}")
                st.error("이미지 표시 중 오류가 발생했습니다.")
        
        # 배치 이미지 표시 (보안 강화)
        if 'batch_images' in st.session_state:
            st.markdown("### 🎪 생성된 동물 컬렉션")
            
            try:
                # 그리드로 안전하게 표시
                cols = st.columns(2)
                for i, img in enumerate(st.session_state.batch_images):
                    if i < 10:  # 최대 10개까지만 표시
                        with cols[i % 2]:
                            st.image(img, caption=f"동물 #{i+1}", use_column_width=True)
            except Exception as e:
                logger.error(f"Batch display error: {e}")
                st.error("배치 이미지 표시 중 오류가 발생했습니다.")
    
    # 사용량 표시 (보안 정보)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 사용량")
    st.sidebar.info(f"이번 세션 요청: {st.session_state.get('request_count', 0)}/{WebAppSecurity.MAX_REQUESTS_PER_HOUR}")
    st.sidebar.info(f"오늘 생성된 이미지: {st.session_state.get('image_count', 0)}/{WebAppSecurity.MAX_IMAGES_PER_DAY}")
    
    # 보안 팁 섹션
    st.markdown("---")
    st.markdown("### 🔒 보안 및 사용 안내")
    
    security_col1, security_col2 = st.columns(2)
    
    with security_col1:
        st.markdown("""
        **🛡️ 보안 기능:**
        - 입력값 자동 검증 및 정화
        - 요청 횟수 제한으로 남용 방지
        - 안전한 파일 처리 및 저장
        - 세션 보안 및 타임아웃
        """)
    
    with security_col2:
        st.markdown("""
        **⚠️ 주의사항:**
        - 부적절한 내용 입력 금지
        - 개인정보 입력하지 마세요
        - 저작권 침해 콘텐츠 금지
        - 상업적 용도 사전 문의 필요
        """)
    
    # 팁 섹션
    st.markdown("### 💡 생성 팁")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        **🎨 더 귀여운 결과를 위해:**
        - "big eyes", "fluffy", "adorable" 키워드 활용
        - 파스텔 컬러나 꽃 배경 언급
        - 액세서리나 포즈 설명 추가
        """)
    
    with tips_col2:
        st.markdown("""
        **⚙️ 설정 최적화:**
        - 생성 품질 높이면 더 디테일한 결과
        - 창의성 조절로 일관성 제어
        - 고화질일수록 생성 시간 증가
        """)
    
    with tips_col3:
        st.markdown("""
        **🐾 추천 조합:**
        - 강아지 + 카와이 스타일
        - 아기 판다 + 치비 스타일  
        - 고양이 + 지브리 스타일
        """)

    # 푸터
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>Made with ❤️ using Stable Diffusion AI | 보안 강화 버전</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"App crashed: {e}")
        st.error("애플리케이션에서 오류가 발생했습니다. 페이지를 새로고침해주세요.")