#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
행렬 덧셈 (Matrix Addition) 구현
Author: AI Assistant
"""

# NumPy 사용 가능 여부 확인
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("=" * 50)
    print("NumPy가 설치되어 있지 않습니다.")
    print("NumPy를 설치하려면 다음 명령어를 사용하세요:")
    print("  pip install numpy")
    print("또는")
    print("  apt install python3-numpy")
    print("=" * 50)


def matrix_addition_pure_python(matrix_a, matrix_b):
    """
    순수 Python으로 행렬 덧셈을 구현
    
    Args:
        matrix_a (list): 첫 번째 행렬 (2차원 리스트)
        matrix_b (list): 두 번째 행렬 (2차원 리스트)
    
    Returns:
        list: 덧셈 결과 행렬
    
    Raises:
        ValueError: 행렬의 크기가 다를 때
    """
    # 행렬의 차원 확인
    rows_a, cols_a = len(matrix_a), len(matrix_a[0])
    rows_b, cols_b = len(matrix_b), len(matrix_b[0])
    
    if rows_a != rows_b or cols_a != cols_b:
        raise ValueError(f"행렬의 크기가 다릅니다: A({rows_a}x{cols_a}) vs B({rows_b}x{cols_b})")
    
    # 결과 행렬 초기화
    result = [[0 for _ in range(cols_a)] for _ in range(rows_a)]
    
    # 행렬 덧셈 수행
    for i in range(rows_a):
        for j in range(cols_a):
            result[i][j] = matrix_a[i][j] + matrix_b[i][j]
    
    return result


def matrix_addition_numpy(matrix_a, matrix_b):
    """
    NumPy를 사용한 행렬 덧셈
    
    Args:
        matrix_a (numpy.ndarray or list): 첫 번째 행렬
        matrix_b (numpy.ndarray or list): 두 번째 행렬
    
    Returns:
        numpy.ndarray: 덧셈 결과 행렬
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy가 설치되어 있지 않습니다.")
    
    # NumPy 배열로 변환
    a = np.array(matrix_a)
    b = np.array(matrix_b)
    
    if a.shape != b.shape:
        raise ValueError(f"행렬의 크기가 다릅니다: A{a.shape} vs B{b.shape}")
    
    return a + b


def print_matrix(matrix, title="행렬"):
    """
    행렬을 보기 좋게 출력하는 함수
    
    Args:
        matrix: 출력할 행렬
        title (str): 행렬의 제목
    """
    print(f"\n{title}:")
    
    # NumPy 배열인 경우 리스트로 변환
    if NUMPY_AVAILABLE and hasattr(matrix, 'tolist'):
        matrix = matrix.tolist()
    
    for row in matrix:
        print("  [", end="")
        for i, val in enumerate(row):
            if i == len(row) - 1:
                print(f"{val:6.2f}", end="")
            else:
                print(f"{val:6.2f},", end=" ")
        print(" ]")


def main():
    """
    메인 함수 - 행렬 덧셈 예제 실행
    """
    print("=" * 50)
    print("         행렬 덧셈 (Matrix Addition)")
    print("=" * 50)
    
    # 예제 행렬 정의
    matrix_a = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    matrix_b = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]
    
    # 입력 행렬 출력
    print_matrix(matrix_a, "행렬 A")
    print_matrix(matrix_b, "행렬 B")
    
    print("\n" + "=" * 50)
    print("1. 순수 Python으로 행렬 덧셈")
    print("=" * 50)
    
    try:
        result_python = matrix_addition_pure_python(matrix_a, matrix_b)
        print_matrix(result_python, "결과 (A + B)")
    except ValueError as e:
        print(f"오류: {e}")
    
    # NumPy 사용 가능한 경우에만 실행
    if NUMPY_AVAILABLE:
        print("\n" + "=" * 50)
        print("2. NumPy를 사용한 행렬 덧셈")
        print("=" * 50)
        
        try:
            result_numpy = matrix_addition_numpy(matrix_a, matrix_b)
            print_matrix(result_numpy, "결과 (A + B)")
        except ValueError as e:
            print(f"오류: {e}")
    else:
        print("\n" + "=" * 50)
        print("2. NumPy를 사용한 행렬 덧셈 (건너뛰기)")
        print("=" * 50)
        print("NumPy가 설치되어 있지 않아 이 섹션을 건너뜁니다.")
    
    # 실수 행렬 예제
    print("\n" + "=" * 50)
    print("3. 실수 행렬 덧셈 예제 (순수 Python)")
    print("=" * 50)
    
    matrix_c = [
        [1.5, 2.7, 3.2],
        [4.1, 5.9, 6.3]
    ]
    
    matrix_d = [
        [0.5, 1.3, 2.8],
        [3.9, 4.1, 5.7]
    ]
    
    print_matrix(matrix_c, "행렬 C")
    print_matrix(matrix_d, "행렬 D")
    
    result_float = matrix_addition_pure_python(matrix_c, matrix_d)
    print_matrix(result_float, "결과 (C + D)")
    
    # 서로 다른 크기 행렬 오류 예제
    print("\n" + "=" * 50)
    print("4. 오류 예제 (크기가 다른 행렬)")
    print("=" * 50)
    
    matrix_e = [[1, 2], [3, 4]]
    matrix_f = [[1, 2, 3], [4, 5, 6]]
    
    print_matrix(matrix_e, "행렬 E (2x2)")
    print_matrix(matrix_f, "행렬 F (2x3)")
    
    try:
        matrix_addition_pure_python(matrix_e, matrix_f)
    except ValueError as e:
        print(f"예상된 오류: {e}")


if __name__ == "__main__":
    main()