import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
import numpy as np
import random
from matplotlib.colors import to_rgba

class AnimalGenerator:
    def __init__(self):
        self.fig_size = (8, 8)
        self.animal_templates = {
            'bear': self.create_bear,
            'cat': self.create_cat,
            'dog': self.create_dog,
            'rabbit': self.create_rabbit,
            'fox': self.create_fox,
            'panda': self.create_panda,
            'pig': self.create_pig,
            'frog': self.create_frog
        }
        
    def create_figure(self, title="귀여운 동물"):
        """새로운 도화지 생성"""
        fig, ax = plt.subplots(1, 1, figsize=self.fig_size)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        return fig, ax
    
    def add_circle(self, ax, x, y, radius, color, alpha=1.0, zorder=1):
        """원 그리기"""
        circle = Circle((x, y), radius, color=color, alpha=alpha, zorder=zorder)
        ax.add_patch(circle)
        return circle
    
    def add_ellipse(self, ax, x, y, width, height, color, alpha=1.0, angle=0, zorder=1):
        """타원 그리기"""
        ellipse = Ellipse((x, y), width, height, color=color, alpha=alpha, angle=angle, zorder=zorder)
        ax.add_patch(ellipse)
        return ellipse
    
    def add_polygon(self, ax, points, color, alpha=1.0, zorder=1):
        """다각형 그리기"""
        polygon = Polygon(points, closed=True, color=color, alpha=alpha, zorder=zorder)
        ax.add_patch(polygon)
        return polygon
    
    def create_bear(self, ax, colors=None):
        """곰 그리기"""
        if colors is None:
            colors = {
                'main': '#8B4513',
                'secondary': '#A0522D', 
                'inner': '#DEB887'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.4, 1.6, colors['main'], zorder=1)
        
        # 머리
        self.add_circle(ax, 5, 5.5, 1.8, colors['main'], zorder=2)
        self.add_circle(ax, 5, 5.5, 1.4, colors['secondary'], zorder=3)
        
        # 귀
        self.add_circle(ax, 3.8, 6.8, 0.7, colors['main'], zorder=2)
        self.add_circle(ax, 6.2, 6.8, 0.7, colors['main'], zorder=2)
        self.add_circle(ax, 3.8, 6.8, 0.5, colors['inner'], zorder=3)
        self.add_circle(ax, 6.2, 6.8, 0.5, colors['inner'], zorder=3)
        
        # 눈
        self.add_circle(ax, 4.4, 5.8, 0.3, 'white', zorder=4)
        self.add_circle(ax, 5.6, 5.8, 0.3, 'white', zorder=4)
        self.add_circle(ax, 4.4, 5.8, 0.2, 'black', zorder=5)
        self.add_circle(ax, 5.6, 5.8, 0.2, 'black', zorder=5)
        
        # 코
        self.add_ellipse(ax, 5, 5.2, 0.3, 0.2, 'black', zorder=4)
        
        # 입
        ax.plot([4.7, 4.9, 5], [4.9, 4.7, 4.8], 'k-', linewidth=3, zorder=4)
        ax.plot([5, 5.1, 5.3], [4.8, 4.7, 4.9], 'k-', linewidth=3, zorder=4)
    
    def create_cat(self, ax, colors=None):
        """고양이 그리기"""
        if colors is None:
            colors = {
                'main': '#FFA500',
                'secondary': '#FFB84D',
                'inner': '#FFF8DC'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.2, 1.4, colors['main'], zorder=1)
        
        # 머리
        self.add_circle(ax, 5, 5.5, 1.6, colors['main'], zorder=2)
        
        # 귀 (삼각형)
        ear1_points = [(3.7, 6.8), (3.2, 7.8), (4.2, 7.3)]
        ear2_points = [(6.3, 6.8), (5.8, 7.3), (6.8, 7.8)]
        self.add_polygon(ax, ear1_points, colors['main'], zorder=3)
        self.add_polygon(ax, ear2_points, colors['main'], zorder=3)
        
        # 귀 안쪽
        inner_ear1 = [(3.75, 6.9), (3.4, 7.4), (4.1, 7.1)]
        inner_ear2 = [(6.25, 6.9), (5.9, 7.1), (6.6, 7.4)]
        self.add_polygon(ax, inner_ear1, colors['inner'], zorder=4)
        self.add_polygon(ax, inner_ear2, colors['inner'], zorder=4)
        
        # 얼굴 패턴
        self.add_ellipse(ax, 5, 5.3, 2.0, 1.6, colors['secondary'], zorder=3)
        
        # 눈 (고양이 특유의)
        self.add_ellipse(ax, 4.4, 5.7, 0.3, 0.6, 'green', zorder=4)
        self.add_ellipse(ax, 5.6, 5.7, 0.3, 0.6, 'green', zorder=4)
        self.add_ellipse(ax, 4.4, 5.7, 0.15, 0.5, 'black', zorder=5)
        self.add_ellipse(ax, 5.6, 5.7, 0.15, 0.5, 'black', zorder=5)
        
        # 코 (삼각형)
        nose_points = [(5, 5.2), (4.8, 4.9), (5.2, 4.9)]
        self.add_polygon(ax, nose_points, 'pink', zorder=4)
        
        # 입
        ax.plot([4.7, 4.9, 5], [4.7, 4.5, 4.6], 'k-', linewidth=2, zorder=4)
        ax.plot([5, 5.1, 5.3], [4.6, 4.5, 4.7], 'k-', linewidth=2, zorder=4)
        
        # 수염
        ax.plot([3.2, 4.0], [5.4, 5.5], 'k-', linewidth=1, zorder=4)
        ax.plot([3.2, 4.0], [5.0, 4.9], 'k-', linewidth=1, zorder=4)
        ax.plot([6.0, 6.8], [5.5, 5.4], 'k-', linewidth=1, zorder=4)
        ax.plot([6.0, 6.8], [4.9, 5.0], 'k-', linewidth=1, zorder=4)
    
    def create_dog(self, ax, colors=None):
        """강아지 그리기"""
        if colors is None:
            colors = {
                'main': '#DEB887',
                'secondary': '#F5DEB3',
                'inner': '#FFF8DC'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.4, 1.6, colors['main'], zorder=1)
        
        # 머리
        self.add_ellipse(ax, 5, 5.5, 1.4, 1.6, colors['main'], zorder=2)
        
        # 귀 (늘어진)
        self.add_ellipse(ax, 3.8, 6.2, 0.6, 1.0, colors['secondary'], zorder=3)
        self.add_ellipse(ax, 6.2, 6.2, 0.6, 1.0, colors['secondary'], zorder=3)
        
        # 주둥이
        self.add_ellipse(ax, 5, 4.8, 0.9, 0.6, colors['inner'], zorder=3)
        
        # 눈
        self.add_circle(ax, 4.5, 5.8, 0.24, 'black', zorder=4)
        self.add_circle(ax, 5.5, 5.8, 0.24, 'black', zorder=4)
        self.add_circle(ax, 4.6, 5.9, 0.08, 'white', zorder=5)
        self.add_circle(ax, 5.6, 5.9, 0.08, 'white', zorder=5)
        
        # 코
        self.add_circle(ax, 5, 5.0, 0.12, 'black', zorder=4)
        
        # 입
        ax.plot([4.7, 4.8, 5], [4.6, 4.3, 4.4], 'k-', linewidth=2, zorder=4)
        ax.plot([5, 5.2, 5.3], [4.4, 4.3, 4.6], 'k-', linewidth=2, zorder=4)
        
        # 혀
        self.add_ellipse(ax, 5, 4.2, 0.3, 0.5, 'pink', zorder=4)
    
    def create_rabbit(self, ax, colors=None):
        """토끼 그리기"""
        if colors is None:
            colors = {
                'main': '#F5F5F5',
                'secondary': '#E6E6FA',
                'inner': '#FFB6C1'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.0, 1.4, colors['main'], zorder=1)
        
        # 머리
        self.add_circle(ax, 5, 5.5, 1.4, colors['main'], zorder=2)
        
        # 긴 귀
        self.add_ellipse(ax, 4.2, 7.2, 0.6, 2.4, colors['main'], zorder=2)
        self.add_ellipse(ax, 5.8, 7.2, 0.6, 2.4, colors['main'], zorder=2)
        self.add_ellipse(ax, 4.2, 7.2, 0.3, 1.6, colors['inner'], zorder=3)
        self.add_ellipse(ax, 5.8, 7.2, 0.3, 1.6, colors['inner'], zorder=3)
        
        # 눈
        self.add_circle(ax, 4.5, 5.7, 0.24, 'black', zorder=4)
        self.add_circle(ax, 5.5, 5.7, 0.24, 'black', zorder=4)
        self.add_circle(ax, 4.6, 5.8, 0.08, 'white', zorder=5)
        self.add_circle(ax, 5.6, 5.8, 0.08, 'white', zorder=5)
        
        # 코 (Y자 모양)
        ax.plot([5, 5], [5.1, 4.9], 'k-', linewidth=2, zorder=4)
        ax.plot([5, 4.85], [5.0, 4.8], 'k-', linewidth=2, zorder=4)
        ax.plot([5, 5.15], [5.0, 4.8], 'k-', linewidth=2, zorder=4)
        
        # 입
        ax.plot([4.85, 5, 5.15], [4.7, 4.6, 4.7], 'k-', linewidth=2, zorder=4)
        
        # 앞니
        rect1 = Rectangle((4.9, 4.5), 0.08, 0.16, color='white', zorder=4)
        rect2 = Rectangle((5.02, 4.5), 0.08, 0.16, color='white', zorder=4)
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.plot([4.9, 4.98, 4.98, 4.9, 4.9], [4.5, 4.5, 4.66, 4.66, 4.5], 'k-', linewidth=0.5)
        ax.plot([5.02, 5.1, 5.1, 5.02, 5.02], [4.5, 4.5, 4.66, 4.66, 4.5], 'k-', linewidth=0.5)
    
    def create_fox(self, ax, colors=None):
        """여우 그리기"""
        if colors is None:
            colors = {
                'main': '#FF8C00',
                'secondary': '#FF7F50',
                'inner': '#FFF8DC'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.2, 1.4, colors['main'], zorder=1)
        
        # 머리 (다이아몬드 모양)
        head_points = [(5, 7), (6.2, 5.5), (5, 4), (3.8, 5.5)]
        self.add_polygon(ax, head_points, colors['main'], zorder=2)
        
        # 귀 (뾰족한)
        ear1_points = [(3.8, 6.5), (3.2, 7.8), (4.4, 7.0)]
        ear2_points = [(6.2, 6.5), (5.6, 7.0), (6.8, 7.8)]
        self.add_polygon(ax, ear1_points, colors['main'], zorder=3)
        self.add_polygon(ax, ear2_points, colors['main'], zorder=3)
        
        # 귀 안쪽 (검은색)
        inner_ear1 = [(3.85, 6.6), (3.5, 7.4), (4.2, 6.9)]
        inner_ear2 = [(6.15, 6.6), (5.8, 6.9), (6.5, 7.4)]
        self.add_polygon(ax, inner_ear1, 'black', zorder=4)
        self.add_polygon(ax, inner_ear2, 'black', zorder=4)
        
        # 얼굴 색상
        face_points = [(5, 6.2), (5.6, 5.5), (5, 4.8), (4.4, 5.5)]
        self.add_polygon(ax, face_points, colors['inner'], zorder=3)
        
        # 눈 (여우 특유의)
        self.add_ellipse(ax, 4.5, 5.7, 0.2, 0.3, '#FFB000', zorder=4)
        self.add_ellipse(ax, 5.5, 5.7, 0.2, 0.3, '#FFB000', zorder=4)
        self.add_ellipse(ax, 4.5, 5.7, 0.1, 0.25, 'black', zorder=5)
        self.add_ellipse(ax, 5.5, 5.7, 0.1, 0.25, 'black', zorder=5)
        
        # 코
        nose_points = [(5, 5.2), (4.9, 5.0), (5.1, 5.0)]
        self.add_polygon(ax, nose_points, 'black', zorder=4)
        
        # 입
        ax.plot([4.8, 4.85, 5], [4.9, 4.7, 4.8], 'k-', linewidth=2, zorder=4)
        ax.plot([5, 5.15, 5.2], [4.8, 4.7, 4.9], 'k-', linewidth=2, zorder=4)
    
    def create_panda(self, ax, colors=None):
        """판다 그리기"""
        if colors is None:
            colors = {
                'main': 'white',
                'secondary': 'black',
                'inner': '#FFF8DC'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.4, 1.6, colors['main'], zorder=1)
        
        # 머리
        self.add_circle(ax, 5, 5.5, 1.6, colors['main'], zorder=2)
        
        # 귀 (검은색)
        self.add_circle(ax, 3.8, 6.8, 0.7, colors['secondary'], zorder=3)
        self.add_circle(ax, 6.2, 6.8, 0.7, colors['secondary'], zorder=3)
        
        # 눈 주위 (검은색)
        self.add_ellipse(ax, 4.4, 5.7, 0.9, 1.2, colors['secondary'], zorder=3)
        self.add_ellipse(ax, 5.6, 5.7, 0.9, 1.2, colors['secondary'], zorder=3)
        
        # 눈
        self.add_circle(ax, 4.4, 5.7, 0.24, 'white', zorder=4)
        self.add_circle(ax, 5.6, 5.7, 0.24, 'white', zorder=4)
        self.add_circle(ax, 4.4, 5.7, 0.16, 'black', zorder=5)
        self.add_circle(ax, 5.6, 5.7, 0.16, 'black', zorder=5)
        
        # 코
        self.add_ellipse(ax, 5, 5.1, 0.24, 0.16, 'black', zorder=4)
        
        # 입
        ax.plot([4.7, 4.85, 5], [4.9, 4.6, 4.7], 'k-', linewidth=2, zorder=4)
        ax.plot([5, 5.15, 5.3], [4.7, 4.6, 4.9], 'k-', linewidth=2, zorder=4)
    
    def create_pig(self, ax, colors=None):
        """돼지 그리기"""
        if colors is None:
            colors = {
                'main': '#FFB6C1',
                'secondary': '#FFC0CB',
                'inner': '#FF69B4'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.6, 1.8, colors['main'], zorder=1)
        
        # 머리
        self.add_circle(ax, 5, 5.5, 1.6, colors['main'], zorder=2)
        
        # 귀 (작은 삼각형)
        ear1_points = [(4.2, 6.7), (3.7, 7.5), (4.6, 7.2)]
        ear2_points = [(5.8, 6.7), (5.4, 7.2), (6.3, 7.5)]
        self.add_polygon(ax, ear1_points, colors['main'], zorder=3)
        self.add_polygon(ax, ear2_points, colors['main'], zorder=3)
        
        # 눈
        self.add_circle(ax, 4.4, 5.7, 0.2, 'black', zorder=4)
        self.add_circle(ax, 5.6, 5.7, 0.2, 'black', zorder=4)
        self.add_circle(ax, 4.5, 5.8, 0.08, 'white', zorder=5)
        self.add_circle(ax, 5.7, 5.8, 0.08, 'white', zorder=5)
        
        # 코 (돼지 특유의)
        self.add_ellipse(ax, 5, 5.0, 0.6, 0.5, colors['inner'], zorder=4)
        self.add_circle(ax, 4.7, 5.0, 0.08, 'black', zorder=5)
        self.add_circle(ax, 5.3, 5.0, 0.08, 'black', zorder=5)
        
        # 입
        ax.plot([4.5, 5, 5.5], [4.6, 4.4, 4.6], 'k-', linewidth=2, zorder=4)
    
    def create_frog(self, ax, colors=None):
        """개구리 그리기"""
        if colors is None:
            colors = {
                'main': '#90EE90',
                'secondary': '#98FB98',
                'inner': '#FFFFE0'
            }
        
        # 몸
        self.add_ellipse(ax, 5, 2.5, 2.8, 1.6, colors['main'], zorder=1)
        
        # 머리
        self.add_ellipse(ax, 5, 5.5, 3.2, 2.8, colors['main'], zorder=2)
        
        # 튀어나온 눈
        self.add_circle(ax, 3.9, 6.8, 0.6, colors['main'], zorder=3)
        self.add_circle(ax, 6.1, 6.8, 0.6, colors['main'], zorder=3)
        self.add_circle(ax, 3.9, 6.8, 0.4, 'white', zorder=4)
        self.add_circle(ax, 6.1, 6.8, 0.4, 'white', zorder=4)
        self.add_circle(ax, 3.9, 6.8, 0.24, 'black', zorder=5)
        self.add_circle(ax, 6.1, 6.8, 0.24, 'black', zorder=5)
        self.add_circle(ax, 4.0, 7.0, 0.08, 'white', zorder=6)
        self.add_circle(ax, 6.2, 7.0, 0.08, 'white', zorder=6)
        
        # 배
        self.add_ellipse(ax, 5, 5.0, 2.0, 1.6, colors['inner'], zorder=3)
        
        # 입 (큰 입)
        ax.plot([3.5, 5, 6.5], [4.8, 4.2, 4.8], 'k-', linewidth=3, zorder=4)
    
    def generate_animal(self, animal_type, colors=None, title=None):
        """지정된 동물 생성"""
        if animal_type not in self.animal_templates:
            print(f"지원하지 않는 동물 타입: {animal_type}")
            return None
        
        if title is None:
            title = f"귀여운 {animal_type.upper()}"
        
        fig, ax = self.create_figure(title)
        
        # 배경 색상 추가
        background_colors = ['#E6F3FF', '#FFE6F3', '#F3FFE6', '#FFF3E6', '#F0E6FF']
        bg_color = random.choice(background_colors)
        ax.add_patch(Rectangle((0, 0), 10, 10, color=bg_color, alpha=0.3, zorder=0))
        
        # 동물 그리기
        self.animal_templates[animal_type](ax, colors)
        
        return fig, ax
    
    def generate_random_animals(self, count=4):
        """랜덤한 동물들 생성"""
        animal_types = list(self.animal_templates.keys())
        
        # 그리드 설정
        cols = int(np.ceil(np.sqrt(count)))
        rows = int(np.ceil(count / cols))
        
        fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 4*rows))
        if count == 1:
            axes = [axes]
        elif rows == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for i in range(count):
            if i < len(axes):
                ax = axes[i]
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                ax.set_aspect('equal')
                ax.axis('off')
                
                # 랜덤 동물 선택
                animal_type = random.choice(animal_types)
                
                # 배경 색상
                background_colors = ['#E6F3FF', '#FFE6F3', '#F3FFE6', '#FFF3E6', '#F0E6FF']
                bg_color = random.choice(background_colors)
                ax.add_patch(Rectangle((0, 0), 10, 10, color=bg_color, alpha=0.3, zorder=0))
                
                # 동물 그리기
                self.animal_templates[animal_type](ax)
                ax.set_title(f"귀여운 {animal_type.upper()}", fontsize=12, fontweight='bold', pad=10)
        
        # 사용하지 않는 subplot 숨기기
        for i in range(count, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        return fig, axes
    
    def show_all_animals(self):
        """모든 동물 종류 보여주기"""
        animal_types = list(self.animal_templates.keys())
        count = len(animal_types)
        
        cols = 4
        rows = int(np.ceil(count / cols))
        
        fig, axes = plt.subplots(rows, cols, figsize=(16, 4*rows))
        axes = axes.flatten()
        
        for i, animal_type in enumerate(animal_types):
            ax = axes[i]
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # 배경 색상
            background_colors = ['#E6F3FF', '#FFE6F3', '#F3FFE6', '#FFF3E6', '#F0E6FF']
            bg_color = background_colors[i % len(background_colors)]
            ax.add_patch(Rectangle((0, 0), 10, 10, color=bg_color, alpha=0.3, zorder=0))
            
            # 동물 그리기
            self.animal_templates[animal_type](ax)
            ax.set_title(f"귀여운 {animal_type.upper()}", fontsize=12, fontweight='bold', pad=10)
        
        # 사용하지 않는 subplot 숨기기
        for i in range(count, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        return fig, axes

def main():
    """메인 함수 - 예제 실행"""
    generator = AnimalGenerator()
    
    print("🐾 귀여운 동물 생성기에 오신 걸 환영합니다! 🐾")
    print("=" * 50)
    
    while True:
        print("\n사용 가능한 옵션:")
        print("1. 특정 동물 생성 (bear, cat, dog, rabbit, fox, panda, pig, frog)")
        print("2. 랜덤 동물들 생성")
        print("3. 모든 동물 보기")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ").strip()
        
        if choice == '1':
            animal_type = input("동물 타입을 입력하세요: ").strip().lower()
            fig, ax = generator.generate_animal(animal_type)
            if fig:
                plt.show()
        
        elif choice == '2':
            try:
                count = int(input("생성할 동물 수를 입력하세요 (1-12): "))
                if 1 <= count <= 12:
                    fig, axes = generator.generate_random_animals(count)
                    plt.show()
                else:
                    print("1-12 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("올바른 숫자를 입력해주세요.")
        
        elif choice == '3':
            fig, axes = generator.show_all_animals()
            plt.show()
        
        elif choice == '4':
            print("안녕히 가세요! 🐾")
            break
        
        else:
            print("올바른 선택을 해주세요.")

if __name__ == "__main__":
    # 간단한 데모 실행
    generator = AnimalGenerator()
    
    # 개별 동물 생성 예제
    print("곰 생성 중...")
    fig, ax = generator.generate_animal('bear')
    plt.savefig('cute_bear.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 랜덤 동물들 생성 예제
    print("랜덤 동물들 생성 중...")
    fig, axes = generator.generate_random_animals(6)
    plt.savefig('random_animals.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 대화형 모드 실행 (선택사항)
    # main()