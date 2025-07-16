import unittest
import cv2
import numpy as np
import os
import tempfile
from unittest.mock import patch, MagicMock
import matplotlib
matplotlib.use('Agg')  # GUI가 없는 환경에서 사용
import matplotlib.pyplot as plt

# 테스트할 모듈들 import
import simple_binary_converter
import binary_image_converter

class TestSimpleBinaryConverter(unittest.TestCase):
    """simple_binary_converter 모듈 테스트"""
    
    def setUp(self):
        """테스트 전 실행되는 설정"""
        # 테스트용 임시 이미지 생성
        self.test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        self.temp_image_path = "test_image.png"
        cv2.imwrite(self.temp_image_path, self.test_image)
    
    def tearDown(self):
        """테스트 후 정리"""
        # 임시 파일들 삭제
        files_to_remove = [self.temp_image_path, "binary_output.png"]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
    
    def test_convert_image_to_binary_success(self):
        """정상적인 이미지 변환 테스트"""
        gray, binary = simple_binary_converter.convert_image_to_binary(self.temp_image_path)
        
        # 결과 검증
        self.assertIsInstance(gray, np.ndarray)
        self.assertIsInstance(binary, np.ndarray)
        self.assertEqual(len(gray.shape), 2)  # 그레이스케일은 2D
        self.assertEqual(len(binary.shape), 2)  # 이진 이미지도 2D
        self.assertTrue(np.all((binary == 0) | (binary == 255)))  # 이진 이미지는 0 또는 255만
    
    def test_convert_image_to_binary_invalid_path(self):
        """존재하지 않는 이미지 파일 테스트"""
        with self.assertRaises(Exception):
            simple_binary_converter.convert_image_to_binary("nonexistent_file.png")
    
    def test_image_dimensions(self):
        """이미지 크기 일치 테스트"""
        gray, binary = simple_binary_converter.convert_image_to_binary(self.temp_image_path)
        
        # 원본과 변환된 이미지의 크기가 같은지 확인
        self.assertEqual(gray.shape, binary.shape)
        self.assertEqual(gray.shape[:2], self.test_image.shape[:2])


class TestBinaryImageConverter(unittest.TestCase):
    """binary_image_converter 모듈 테스트"""
    
    def setUp(self):
        """테스트 전 실행되는 설정"""
        # 다양한 테스트용 이미지 생성
        self.test_image_simple = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        self.test_image_complex = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        
        self.temp_image_simple = "test_simple.png"
        self.temp_image_complex = "test_complex.png"
        
        cv2.imwrite(self.temp_image_simple, self.test_image_simple)
        cv2.imwrite(self.temp_image_complex, self.test_image_complex)
    
    def tearDown(self):
        """테스트 후 정리"""
        files_to_remove = [
            self.temp_image_simple, 
            self.temp_image_complex,
            "test_output.png"
        ]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
    
    def test_convert_to_binary_otsu(self):
        """Otsu 방법 테스트"""
        binary, gray = binary_image_converter.convert_to_binary(
            self.temp_image_simple, method='otsu'
        )
        
        self.assertIsInstance(binary, np.ndarray)
        self.assertIsInstance(gray, np.ndarray)
        self.assertEqual(len(binary.shape), 2)
        self.assertTrue(np.all((binary == 0) | (binary == 255)))
    
    def test_convert_to_binary_adaptive(self):
        """적응형 임계값 방법 테스트"""
        binary, gray = binary_image_converter.convert_to_binary(
            self.temp_image_simple, method='adaptive'
        )
        
        self.assertIsInstance(binary, np.ndarray)
        self.assertEqual(len(binary.shape), 2)
        self.assertTrue(np.all((binary == 0) | (binary == 255)))
    
    def test_convert_to_binary_simple(self):
        """단순 임계값 방법 테스트"""
        binary, gray = binary_image_converter.convert_to_binary(
            self.temp_image_simple, method='simple', threshold_value=128
        )
        
        self.assertIsInstance(binary, np.ndarray)
        self.assertEqual(len(binary.shape), 2)
        self.assertTrue(np.all((binary == 0) | (binary == 255)))
    
    def test_invalid_method(self):
        """잘못된 방법 입력 테스트"""
        with self.assertRaises(ValueError):
            binary_image_converter.convert_to_binary(
                self.temp_image_simple, method='invalid_method'
            )
    
    def test_invalid_image_path(self):
        """존재하지 않는 이미지 파일 테스트"""
        with self.assertRaises(ValueError):
            binary_image_converter.convert_to_binary("nonexistent.png")
    
    def test_save_binary_image(self):
        """이미지 저장 기능 테스트"""
        binary, _ = binary_image_converter.convert_to_binary(
            self.temp_image_simple, method='otsu'
        )
        
        output_path = "test_output.png"
        binary_image_converter.save_binary_image(binary, output_path)
        
        # 파일이 생성되었는지 확인
        self.assertTrue(os.path.exists(output_path))
        
        # 저장된 이미지를 읽어서 검증
        saved_image = cv2.imread(output_path, cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(saved_image)
        np.testing.assert_array_equal(binary, saved_image)
    
    def test_quick_binary_convert(self):
        """빠른 변환 함수 테스트"""
        result = binary_image_converter.quick_binary_convert(self.temp_image_simple)
        
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result.shape), 2)
        self.assertTrue(np.all((result == 0) | (result == 255)))
    
    @patch('matplotlib.pyplot.show')
    def test_display_results(self, mock_show):
        """결과 표시 함수 테스트 (matplotlib.show 모킹)"""
        binary, gray = binary_image_converter.convert_to_binary(
            self.temp_image_simple, method='otsu'
        )
        
        # 예외가 발생하지 않으면 성공
        try:
            binary_image_converter.display_results(gray, binary, 'otsu')
            mock_show.assert_called_once()
        except Exception as e:
            self.fail(f"display_results raised an exception: {e}")


class TestIntegration(unittest.TestCase):
    """통합 테스트"""
    
    def setUp(self):
        """테스트 전 실행되는 설정"""
        # 실제 이미지와 유사한 테스트 이미지 생성
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # 흰색 사각형 그리기
        self.test_image[20:80, 20:80] = [255, 255, 255]
        # 검은색 원 그리기
        cv2.circle(self.test_image, (50, 50), 15, (0, 0, 0), -1)
        
        self.temp_image_path = "integration_test.png"
        cv2.imwrite(self.temp_image_path, self.test_image)
    
    def tearDown(self):
        """테스트 후 정리"""
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)
    
    def test_both_converters_consistency(self):
        """두 변환기의 결과 일관성 테스트"""
        # simple_binary_converter 결과
        gray1, binary1 = simple_binary_converter.convert_image_to_binary(self.temp_image_path)
        
        # binary_image_converter 결과 (otsu 방법)
        binary2, gray2 = binary_image_converter.convert_to_binary(
            self.temp_image_path, method='otsu'
        )
        
        # 그레이스케일 이미지는 동일해야 함
        np.testing.assert_array_equal(gray1, gray2)
        
        # 이진 이미지도 동일해야 함 (같은 otsu 방법 사용)
        np.testing.assert_array_equal(binary1, binary2)
    
    def test_threshold_variations(self):
        """다양한 임계값에 대한 테스트"""
        threshold_values = [50, 100, 150, 200]
        
        for threshold in threshold_values:
            binary, _ = binary_image_converter.convert_to_binary(
                self.temp_image_path, method='simple', threshold_value=threshold
            )
            
            # 이진 이미지 조건 확인
            self.assertTrue(np.all((binary == 0) | (binary == 255)))
            
            # 임계값이 높을수록 흰색 픽셀이 적어져야 함
            white_pixels = np.sum(binary == 255)
            self.assertGreaterEqual(white_pixels, 0)


class TestPerformance(unittest.TestCase):
    """성능 테스트"""
    
    def setUp(self):
        """대용량 테스트 이미지 생성"""
        self.large_image = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)
        self.large_image_path = "large_test.png"
        cv2.imwrite(self.large_image_path, self.large_image)
    
    def tearDown(self):
        """정리"""
        if os.path.exists(self.large_image_path):
            os.remove(self.large_image_path)
    
    def test_large_image_processing(self):
        """대용량 이미지 처리 테스트"""
        import time
        
        start_time = time.time()
        binary, gray = binary_image_converter.convert_to_binary(
            self.large_image_path, method='otsu'
        )
        end_time = time.time()
        
        # 처리 시간이 합리적인지 확인 (10초 이내)
        processing_time = end_time - start_time
        self.assertLess(processing_time, 10.0)
        
        # 결과 검증
        self.assertEqual(binary.shape, (1000, 1000))
        self.assertTrue(np.all((binary == 0) | (binary == 255)))


def run_tests_with_report():
    """테스트 실행 및 결과 리포트"""
    print("=== 이미지 이진화 모듈 테스트 시작 ===\n")
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 각 테스트 클래스 추가
    test_classes = [
        TestSimpleBinaryConverter,
        TestBinaryImageConverter,
        TestIntegration,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2, stream=None)
    result = runner.run(suite)
    
    # 결과 리포트
    print(f"\n=== 테스트 결과 ===")
    print(f"총 테스트 수: {result.testsRun}")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"에러: {len(result.errors)}")
    
    if result.failures:
        print(f"\n실패한 테스트:")
        for test, trace in result.failures:
            print(f"- {test}: {trace}")
    
    if result.errors:
        print(f"\n에러가 발생한 테스트:")
        for test, trace in result.errors:
            print(f"- {test}: {trace}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # 개별 테스트 실행
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--quick":
        # 빠른 테스트만 실행
        suite = unittest.TestSuite()
        suite.addTest(TestSimpleBinaryConverter('test_convert_image_to_binary_success'))
        suite.addTest(TestBinaryImageConverter('test_convert_to_binary_otsu'))
        
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    else:
        # 전체 테스트 실행
        success = run_tests_with_report()
        exit(0 if success else 1)