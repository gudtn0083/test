#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
음성 인식 시스템 사용 예제
"""

from speech_recognition_system import SpeechRecognitionSystem

def main():
    print("=== 음성 인식 시스템 사용 예제 ===")
    
    # 음성 인식 시스템 초기화
    srs = SpeechRecognitionSystem()
    
    # 예제 1: 단일 파일 처리
    print("\n1. 단일 파일 처리 예제")
    audio_file = "example.wav"  # 실제 오디오 파일 경로로 변경
    
    if input(f"'{audio_file}' 파일을 처리하시겠습니까? (y/n): ").lower() == 'y':
        result = srs.process_audio_file(audio_file, method='google', language='ko-KR')
        print(f"인식 결과: {result}")
    
    # 예제 2: 다른 언어로 인식
    print("\n2. 영어 음성 인식 예제")
    english_file = "english_audio.wav"  # 실제 영어 오디오 파일 경로로 변경
    
    if input(f"'{english_file}' 파일을 영어로 처리하시겠습니까? (y/n): ").lower() == 'y':
        result = srs.process_audio_file(english_file, method='google', language='en-US')
        print(f"인식 결과: {result}")
    
    # 예제 3: 오프라인 인식
    print("\n3. 오프라인 음성 인식 예제")
    
    if input("오프라인 인식을 시도하시겠습니까? (y/n): ").lower() == 'y':
        result = srs.process_audio_file(audio_file, method='offline')
        print(f"오프라인 인식 결과: {result}")
    
    # 예제 4: 일괄 처리
    print("\n4. 일괄 처리 예제")
    audio_dir = "./audio_files"  # 오디오 파일들이 있는 디렉토리 경로
    
    if input(f"'{audio_dir}' 디렉토리의 모든 오디오 파일을 처리하시겠습니까? (y/n): ").lower() == 'y':
        results = srs.batch_process(audio_dir, "recognition_results.txt")
        print(f"일괄 처리 완료: {len(results)}개 파일 처리됨")
    
    print("\n=== 예제 완료 ===")

if __name__ == "__main__":
    main()