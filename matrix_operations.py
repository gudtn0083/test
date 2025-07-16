#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
행렬 연산 (Matrix Operations) 구현 - 덧셈, 뺄셈, 곱셈
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


def matrix_multiplication_pure_python(matrix_a, matrix_b):
    """
    순수 Python으로 행렬 곱셈을 구현
    
    Args:
        matrix_a (list): 첫 번째 행렬 (2차원 리스트)
        matrix_b (list): 두 번째 행렬 (2차원 리스트)
    
    Returns:
        list: 곱셈 결과 행렬 (A × B)
    
    Raises:
        ValueError: 행렬 곱셈이 불가능할 때 (A의 열 수 ≠ B의 행 수)
    """
    # 행렬의 차원 확인
    rows_a, cols_a = len(matrix_a), len(matrix_a[0])
    rows_b, cols_b = len(matrix_b), len(matrix_b[0])
    
    if cols_a != rows_b:
        raise ValueError(f"행렬 곱셈이 불가능합니다: A({rows_a}x{cols_a}) × B({rows_b}x{cols_b}). A의 열 수와 B의 행 수가 같아야 합니다.")
    
    # 결과 행렬 초기화 (rows_a × cols_b)
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    
    # 행렬 곱셈 수행
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    
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


def matrix_multiplication_numpy(matrix_a, matrix_b):
    """
    NumPy를 사용한 행렬 곱셈
    
    Args:
        matrix_a (numpy.ndarray or list): 첫 번째 행렬
        matrix_b (numpy.ndarray or list): 두 번째 행렬
    
    Returns:
        numpy.ndarray: 곱셈 결과 행렬 (A × B)
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy가 설치되어 있지 않습니다.")
    
    # NumPy 배열로 변환
    a = np.array(matrix_a)
    b = np.array(matrix_b)
    
    if a.shape[1] != b.shape[0]:
        raise ValueError(f"행렬 곱셈이 불가능합니다: A{a.shape} × B{b.shape}. A의 열 수와 B의 행 수가 같아야 합니다.")
    
    return np.dot(a, b)


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


def print_matrix_dimensions(matrix, name="행렬"):
    """
    행렬의 차원을 출력하는 함수
    
    Args:
        matrix: 차원을 확인할 행렬
        name (str): 행렬의 이름
    """
    if NUMPY_AVAILABLE and hasattr(matrix, 'shape'):
        rows, cols = matrix.shape
    else:
        rows, cols = len(matrix), len(matrix[0])
    print(f"{name} 차원: {rows}×{cols}")


def main():
    """
    메인 함수 - 행렬 덧셈, 뺄셈, 곱셈 예제 실행
    """
    print("=" * 70)
    print("            행렬 연산 (Matrix Operations)")
    print("             덧셈, 뺄셈, 곱셈")
    print("=" * 70)
    
    # 예제 행렬 정의 (곱셈용)
    matrix_a = [
        [1, 2, 3],
        [4, 5, 6]
    ]  # 2×3 행렬
    
    matrix_b = [
        [7, 8],
        [9, 10],
        [11, 12]
    ]  # 3×2 행렬
    
    # 입력 행렬 출력
    print_matrix(matrix_a, "행렬 A (2×3)")
    print_matrix_dimensions(matrix_a, "A")
    print_matrix(matrix_b, "행렬 B (3×2)")
    print_matrix_dimensions(matrix_b, "B")
    
    print("\n" + "=" * 70)
    print("1. 순수 Python으로 행렬 곱셈 (A × B)")
    print("=" * 70)
    
    try:
        result_mul_python = matrix_multiplication_pure_python(matrix_a, matrix_b)
        print_matrix(result_mul_python, "결과 (A × B)")
        print_matrix_dimensions(result_mul_python, "결과")
    except ValueError as e:
        print(f"오류: {e}")
    
    # NumPy 사용 가능한 경우에만 실행
    if NUMPY_AVAILABLE:
        print("\n" + "=" * 70)
        print("2. NumPy를 사용한 행렬 곱셈 (A × B)")
        print("=" * 70)
        
        try:
            result_mul_numpy = matrix_multiplication_numpy(matrix_a, matrix_b)
            print_matrix(result_mul_numpy, "결과 (A × B)")
            print_matrix_dimensions(result_mul_numpy, "결과")
        except ValueError as e:
            print(f"오류: {e}")
    else:
        print("\n" + "=" * 70)
        print("2. NumPy를 사용한 행렬 곱셈 (건너뛰기)")
        print("=" * 70)
        print("NumPy가 설치되어 있지 않아 이 섹션을 건너뜁니다.")
    
    # 정사각 행렬 예제
    print("\n" + "=" * 70)
    print("3. 정사각 행렬 곱셈 예제")
    print("=" * 70)
    
    matrix_c = [
        [1, 2],
        [3, 4]
    ]  # 2×2 행렬
    
    matrix_d = [
        [5, 6],
        [7, 8]
    ]  # 2×2 행렬
    
    print_matrix(matrix_c, "행렬 C (2×2)")
    print_matrix(matrix_d, "행렬 D (2×2)")
    
    result_square = matrix_multiplication_pure_python(matrix_c, matrix_d)
    print_matrix(result_square, "결과 (C × D)")
    
    # 벡터와 행렬 곱셈
    print("\n" + "=" * 70)
    print("4. 벡터와 행렬 곱셈 예제")
    print("=" * 70)
    
    matrix_e = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]  # 3×3 행렬
    
    vector_f = [
        [2],
        [1],
        [3]
    ]  # 3×1 벡터
    
    print_matrix(matrix_e, "행렬 E (3×3)")
    print_matrix(vector_f, "벡터 F (3×1)")
    
    result_vector = matrix_multiplication_pure_python(matrix_e, vector_f)
    print_matrix(result_vector, "결과 (E × F)")
    
    # 덧셈과 뺄셈 예제 (동일한 크기 행렬)
    print("\n" + "=" * 70)
    print("5. 같은 크기 행렬의 덧셈과 뺄셈")
    print("=" * 70)
    
    print_matrix(matrix_c, "행렬 C")
    print_matrix(matrix_d, "행렬 D")
    
    result_add = matrix_addition_pure_python(matrix_c, matrix_d)
    print_matrix(result_add, "덧셈 결과 (C + D)")
    
    result_sub = matrix_subtraction_pure_python(matrix_c, matrix_d)
    print_matrix(result_sub, "뺄셈 결과 (C - D)")
    
    # 실수 행렬 곱셈
    print("\n" + "=" * 70)
    print("6. 실수 행렬 곱셈 예제")
    print("=" * 70)
    
    matrix_g = [
        [1.5, 2.0],
        [3.5, 4.0]
    ]
    
    matrix_h = [
        [2.0, 1.5],
        [1.0, 2.5]
    ]
    
    print_matrix(matrix_g, "행렬 G")
    print_matrix(matrix_h, "행렬 H")
    
    result_float_mul = matrix_multiplication_pure_python(matrix_g, matrix_h)
    print_matrix(result_float_mul, "결과 (G × H)")
    
    # 곱셈 불가능한 경우 오류 예제
    print("\n" + "=" * 70)
    print("7. 오류 예제 (곱셈 불가능한 행렬)")
    print("=" * 70)
    
    matrix_i = [[1, 2], [3, 4]]  # 2×2
    matrix_j = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # 3×3
    
    print_matrix(matrix_i, "행렬 I (2×2)")
    print_matrix(matrix_j, "행렬 J (3×3)")
    
    try:
        matrix_multiplication_pure_python(matrix_i, matrix_j)
    except ValueError as e:
        print(f"예상된 오류 (곱셈): {e}")


if __name__ == "__main__":
    main()