import streamlit as st
import torch
from PIL import Image
import io
import base64
from cute_animal_generator import CuteAnimalGenerator, quick_generate
import time
import os

# 페이지 설정
st.set_page_config(
    page_title="🐾 귀여운 동물 AI 생성기",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .animal-card {
        border: 2px solid #ffb6c1;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #fff5f5;
    }
    .stButton > button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 154, 158, 0.4);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_generator():
    """AI 생성기 로드 (캐시됨)"""
    return CuteAnimalGenerator()

def image_to_base64(image):
    """이미지를 base64로 변환"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def main():
    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🐾 귀여운 동물 AI 이미지 생성기 🐾</h1>
        <p>AI가 만드는 세상에서 가장 귀여운 동물 친구들을 만나보세요!</p>
    </div>
    """, unsafe_allow_html=True)

    # 사이드바 설정
    st.sidebar.markdown("## 🎨 생성 설정")
    
    # 동물 선택
    animal_types = [
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
    
    selected_animal = st.sidebar.selectbox("🐾 동물 선택", animal_types)
    
    # 스타일 설정
    style_options = [
        "자동 선택", "카와이 스타일", "치비 스타일", "만화 스타일", 
        "애니메이션 스타일", "픽사 스타일", "디즈니 스타일", "지브리 스타일"
    ]
    
    selected_style = st.sidebar.selectbox("🎨 스타일 선택", style_options)
    
    # 고급 설정
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
    
    num_steps = st.sidebar.slider("🔄 생성 품질", min_value=10, max_value=50, value=20)
    guidance_scale = st.sidebar.slider("🎯 창의성 조절", min_value=5.0, max_value=15.0, value=7.5, step=0.5)
    
    # 커스텀 프롬프트
    st.sidebar.markdown("### ✍️ 커스텀 프롬프트")
    custom_prompt = st.sidebar.text_area(
        "원하는 상세 설명을 입력하세요",
        placeholder="예: 분홍색 리본을 한 하얀 강아지가 꽃밭에서 뛰어놀고 있어요"
    )
    
    # 메인 컨텐츠
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 이미지 생성")
        
        # 생성 버튼
        if st.button("🎨 귀여운 동물 생성하기!", key="generate_single"):
            if 'generator' not in st.session_state:
                with st.spinner("AI 모델을 로딩 중입니다... (최초 실행시 시간이 걸릴 수 있습니다)"):
                    st.session_state.generator = load_generator()
            
            with st.spinner("귀여운 동물을 생성 중입니다... 🎨"):
                try:
                    generator = st.session_state.generator
                    
                    # 프롬프트 설정
                    if custom_prompt:
                        prompt = custom_prompt
                        if selected_style != "자동 선택":
                            prompt += f", {selected_style.replace(' 스타일', ' style')}"
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
                    
                    # 세션 상태에 저장
                    st.session_state.generated_image = final_image
                    st.session_state.generation_time = time.time()
                    
                    st.success("✨ 귀여운 동물이 생성되었습니다!")
                    
                except Exception as e:
                    st.error(f"생성 중 오류가 발생했습니다: {str(e)}")
        
        # 배치 생성
        st.markdown("### 🎪 배치 생성")
        batch_count = st.slider("생성할 이미지 수", min_value=2, max_value=6, value=4)
        
        if st.button("🎪 여러 동물 한번에 생성하기!", key="generate_batch"):
            if 'generator' not in st.session_state:
                with st.spinner("AI 모델을 로딩 중입니다..."):
                    st.session_state.generator = load_generator()
            
            with st.spinner(f"{batch_count}마리의 귀여운 동물들을 생성 중입니다..."):
                try:
                    generator = st.session_state.generator
                    
                    # 배치 생성
                    batch_images = []
                    for i in range(batch_count):
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
                    
                    st.session_state.batch_images = batch_images
                    st.success(f"✨ {batch_count}마리의 귀여운 동물들이 생성되었습니다!")
                    
                except Exception as e:
                    st.error(f"배치 생성 중 오류가 발생했습니다: {str(e)}")
    
    with col2:
        st.markdown("### 🖼️ 생성된 이미지")
        
        # 단일 이미지 표시
        if 'generated_image' in st.session_state:
            st.image(
                st.session_state.generated_image,
                caption="생성된 귀여운 동물 🐾",
                use_column_width=True
            )
            
            # 다운로드 버튼
            buffer = io.BytesIO()
            st.session_state.generated_image.save(buffer, format="PNG")
            st.download_button(
                label="💾 이미지 다운로드",
                data=buffer.getvalue(),
                file_name=f"cute_animal_{int(st.session_state.generation_time)}.png",
                mime="image/png"
            )
        
        # 배치 이미지 표시
        if 'batch_images' in st.session_state:
            st.markdown("### 🎪 생성된 동물 컬렉션")
            
            # 그리드로 표시
            cols = st.columns(2)
            for i, img in enumerate(st.session_state.batch_images):
                with cols[i % 2]:
                    st.image(img, caption=f"동물 #{i+1}", use_column_width=True)
    
    # 팁 섹션
    st.markdown("---")
    st.markdown("### 💡 생성 팁")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        **🎨 더 귀여운 결과를 위해:**
        - 커스텀 프롬프트에 "big eyes", "fluffy", "adorable" 같은 단어 추가
        - 파스텔 컬러나 꽃 등의 배경 요소 언급
        """)
    
    with tips_col2:
        st.markdown("""
        **⚙️ 설정 조절:**
        - 생성 품질을 높이면 더 디테일한 이미지
        - 창의성을 낮추면 더 일관된 결과
        - 고화질일수록 생성 시간 증가
        """)
    
    with tips_col3:
        st.markdown("""
        **🐾 추천 동물:**
        - 강아지, 고양이: 가장 안정적인 결과
        - 아기 동물들: 자연스럽게 귀여운 느낌
        - 특이한 동물: 창의적이고 독특한 결과
        """)

    # 푸터
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>Made with ❤️ using Stable Diffusion AI</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()