#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
행렬 연산 (Matrix Operations) 구현 - 덧셈과 뺄셈
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


def matrix_subtraction_pure_python(matrix_a, matrix_b):
    """
    순수 Python으로 행렬 뺄셈을 구현
    
    Args:
        matrix_a (list): 첫 번째 행렬 (2차원 리스트)
        matrix_b (list): 두 번째 행렬 (2차원 리스트)
    
    Returns:
        list: 뺄셈 결과 행렬 (A - B)
    
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
    
    # 행렬 뺄셈 수행
    for i in range(rows_a):
        for j in range(cols_a):
            result[i][j] = matrix_a[i][j] - matrix_b[i][j]
    
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


def matrix_subtraction_numpy(matrix_a, matrix_b):
    """
    NumPy를 사용한 행렬 뺄셈
    
    Args:
        matrix_a (numpy.ndarray or list): 첫 번째 행렬
        matrix_b (numpy.ndarray or list): 두 번째 행렬
    
    Returns:
        numpy.ndarray: 뺄셈 결과 행렬 (A - B)
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy가 설치되어 있지 않습니다.")
    
    # NumPy 배열로 변환
    a = np.array(matrix_a)
    b = np.array(matrix_b)
    
    if a.shape != b.shape:
        raise ValueError(f"행렬의 크기가 다릅니다: A{a.shape} vs B{b.shape}")
    
    return a - b


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
    메인 함수 - 행렬 덧셈과 뺄셈 예제 실행
    """
    print("=" * 60)
    print("         행렬 연산 (Matrix Operations)")
    print("            덧셈과 뺄셈")
    print("=" * 60)
    
    # 예제 행렬 정의
    matrix_a = [
        [10, 8, 6],
        [4, 2, 9],
        [7, 5, 3]
    ]
    
    matrix_b = [
        [2, 3, 1],
        [1, 1, 4],
        [3, 2, 1]
    ]
    
    # 입력 행렬 출력
    print_matrix(matrix_a, "행렬 A")
    print_matrix(matrix_b, "행렬 B")
    
    print("\n" + "=" * 60)
    print("1. 순수 Python으로 행렬 덧셈")
    print("=" * 60)
    
    try:
        result_add_python = matrix_addition_pure_python(matrix_a, matrix_b)
        print_matrix(result_add_python, "결과 (A + B)")
    except ValueError as e:
        print(f"오류: {e}")
    
    print("\n" + "=" * 60)
    print("2. 순수 Python으로 행렬 뺄셈")
    print("=" * 60)
    
    try:
        result_sub_python = matrix_subtraction_pure_python(matrix_a, matrix_b)
        print_matrix(result_sub_python, "결과 (A - B)")
    except ValueError as e:
        print(f"오류: {e}")
    
    # NumPy 사용 가능한 경우에만 실행
    if NUMPY_AVAILABLE:
        print("\n" + "=" * 60)
        print("3. NumPy를 사용한 행렬 덧셈")
        print("=" * 60)
        
        try:
            result_add_numpy = matrix_addition_numpy(matrix_a, matrix_b)
            print_matrix(result_add_numpy, "결과 (A + B)")
        except ValueError as e:
            print(f"오류: {e}")
        
        print("\n" + "=" * 60)
        print("4. NumPy를 사용한 행렬 뺄셈")
        print("=" * 60)
        
        try:
            result_sub_numpy = matrix_subtraction_numpy(matrix_a, matrix_b)
            print_matrix(result_sub_numpy, "결과 (A - B)")
        except ValueError as e:
            print(f"오류: {e}")
    else:
        print("\n" + "=" * 60)
        print("3-4. NumPy를 사용한 행렬 연산 (건너뛰기)")
        print("=" * 60)
        print("NumPy가 설치되어 있지 않아 이 섹션을 건너뜁니다.")
    
    # 실수 행렬 예제
    print("\n" + "=" * 60)
    print("5. 실수 행렬 연산 예제 (순수 Python)")
    print("=" * 60)
    
    matrix_c = [
        [5.5, 3.2, 8.1],
        [2.7, 6.9, 4.3]
    ]
    
    matrix_d = [
        [1.5, 2.2, 3.1],
        [1.7, 3.9, 2.3]
    ]
    
    print_matrix(matrix_c, "행렬 C")
    print_matrix(matrix_d, "행렬 D")
    
    result_add_float = matrix_addition_pure_python(matrix_c, matrix_d)
    print_matrix(result_add_float, "결과 (C + D)")
    
    result_sub_float = matrix_subtraction_pure_python(matrix_c, matrix_d)
    print_matrix(result_sub_float, "결과 (C - D)")
    
    # 음수 결과 예제
    print("\n" + "=" * 60)
    print("6. 음수 결과를 포함한 예제")
    print("=" * 60)
    
    matrix_e = [
        [1, 2],
        [3, 4]
    ]
    
    matrix_f = [
        [5, 6],
        [7, 8]
    ]
    
    print_matrix(matrix_e, "행렬 E")
    print_matrix(matrix_f, "행렬 F")
    
    result_sub_negative = matrix_subtraction_pure_python(matrix_e, matrix_f)
    print_matrix(result_sub_negative, "결과 (E - F) - 음수 포함")
    
    # 서로 다른 크기 행렬 오류 예제
    print("\n" + "=" * 60)
    print("7. 오류 예제 (크기가 다른 행렬)")
    print("=" * 60)
    
    matrix_g = [[1, 2], [3, 4]]
    matrix_h = [[1, 2, 3], [4, 5, 6]]
    
    print_matrix(matrix_g, "행렬 G (2x2)")
    print_matrix(matrix_h, "행렬 H (2x3)")
    
    try:
        matrix_subtraction_pure_python(matrix_g, matrix_h)
    except ValueError as e:
        print(f"예상된 오류 (뺄셈): {e}")


if __name__ == "__main__":
    main()