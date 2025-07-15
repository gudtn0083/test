#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import os
import sys
from pydub import AudioSegment
from pydub.utils import which
import tempfile
import argparse
from pathlib import Path

class SpeechRecognitionSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # 지원하는 오디오 포맷
        self.supported_formats = ['.wav', '.mp3', '.mp4', '.m4a', '.flac', '.aac', '.ogg', '.wma']
        
    def convert_to_wav(self, input_file):
        """다양한 오디오 포맷을 WAV로 변환"""
        try:
            # 파일 확장자 확인
            file_extension = Path(input_file).suffix.lower()
            
            if file_extension == '.wav':
                return input_file
            
            # 오디오 파일 로드
            if file_extension == '.mp3':
                audio = AudioSegment.from_mp3(input_file)
            elif file_extension == '.mp4':
                audio = AudioSegment.from_file(input_file, format="mp4")
            elif file_extension == '.m4a':
                audio = AudioSegment.from_file(input_file, format="m4a")
            elif file_extension == '.flac':
                audio = AudioSegment.from_file(input_file, format="flac")
            elif file_extension == '.aac':
                audio = AudioSegment.from_file(input_file, format="aac")
            elif file_extension == '.ogg':
                audio = AudioSegment.from_file(input_file, format="ogg")
            elif file_extension == '.wma':
                audio = AudioSegment.from_file(input_file, format="wma")
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {file_extension}")
            
            # 임시 WAV 파일 생성
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            audio.export(temp_wav.name, format="wav")
            return temp_wav.name
            
        except Exception as e:
            print(f"오디오 변환 중 오류 발생: {str(e)}")
            return None
    
    def recognize_speech_google(self, audio_file, language='ko-KR'):
        """Google Speech Recognition을 사용한 음성 인식"""
        try:
            with sr.AudioFile(audio_file) as source:
                # 잡음 제거
                self.recognizer.adjust_for_ambient_noise(source)
                # 오디오 데이터 읽기
                audio_data = self.recognizer.record(source)
                
                # Google Speech Recognition 사용
                text = self.recognizer.recognize_google(audio_data, language=language)
                return text
                
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"Google Speech Recognition 서비스에 오류가 발생했습니다: {str(e)}"
        except Exception as e:
            return f"음성 인식 중 오류 발생: {str(e)}"
    
    def recognize_speech_offline(self, audio_file):
        """오프라인 음성 인식 (PocketSphinx 사용)"""
        try:
            with sr.AudioFile(audio_file) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio_data = self.recognizer.record(source)
                
                # PocketSphinx 사용 (오프라인)
                text = self.recognizer.recognize_sphinx(audio_data)
                return text
                
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"PocketSphinx 오류: {str(e)}"
        except Exception as e:
            return f"음성 인식 중 오류 발생: {str(e)}"
    
    def process_audio_file(self, file_path, method='google', language='ko-KR'):
        """오디오 파일 처리 및 음성 인식"""
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            return f"파일을 찾을 수 없습니다: {file_path}"
        
        # 파일 확장자 확인
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in self.supported_formats:
            return f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(self.supported_formats)}"
        
        print(f"파일 처리 중: {file_path}")
        
        # WAV 형식으로 변환
        wav_file = self.convert_to_wav(file_path)
        if wav_file is None:
            return "오디오 파일 변환에 실패했습니다."
        
        try:
            # 음성 인식 수행
            if method == 'google':
                result = self.recognize_speech_google(wav_file, language)
            elif method == 'offline':
                result = self.recognize_speech_offline(wav_file)
            else:
                result = "알 수 없는 인식 방법입니다."
            
            # 임시 파일 정리
            if wav_file != file_path and os.path.exists(wav_file):
                os.unlink(wav_file)
            
            return result
            
        except Exception as e:
            # 임시 파일 정리
            if wav_file != file_path and os.path.exists(wav_file):
                os.unlink(wav_file)
            return f"처리 중 오류 발생: {str(e)}"
    
    def batch_process(self, directory_path, output_file=None):
        """디렉토리 내 모든 오디오 파일을 일괄 처리"""
        results = []
        
        if not os.path.exists(directory_path):
            return f"디렉토리를 찾을 수 없습니다: {directory_path}"
        
        # 디렉토리 내 오디오 파일 찾기
        audio_files = []
        for ext in self.supported_formats:
            audio_files.extend(Path(directory_path).glob(f"*{ext}"))
        
        if not audio_files:
            return "디렉토리에 오디오 파일이 없습니다."
        
        print(f"발견된 오디오 파일: {len(audio_files)}개")
        
        for audio_file in audio_files:
            print(f"\n처리 중: {audio_file.name}")
            result = self.process_audio_file(str(audio_file))
            results.append({
                'file': audio_file.name,
                'result': result
            })
        
        # 결과 출력
        print("\n=== 처리 결과 ===")
        for result in results:
            print(f"\n파일: {result['file']}")
            print(f"결과: {result['result']}")
        
        # 파일로 저장
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("음성 인식 결과\n")
                f.write("=" * 50 + "\n\n")
                for result in results:
                    f.write(f"파일: {result['file']}\n")
                    f.write(f"결과: {result['result']}\n")
                    f.write("-" * 30 + "\n")
            print(f"\n결과가 파일에 저장되었습니다: {output_file}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='음성 파일 인식 시스템')
    parser.add_argument('input', help='입력 파일 또는 디렉토리 경로')
    parser.add_argument('--method', choices=['google', 'offline'], default='google',
                        help='음성 인식 방법 (기본값: google)')
    parser.add_argument('--language', default='ko-KR',
                        help='언어 코드 (기본값: ko-KR)')
    parser.add_argument('--output', help='결과 저장 파일 경로')
    parser.add_argument('--batch', action='store_true',
                        help='디렉토리 내 모든 오디오 파일 일괄 처리')
    
    args = parser.parse_args()
    
    # 음성 인식 시스템 초기화
    srs = SpeechRecognitionSystem()
    
    if args.batch:
        # 일괄 처리
        results = srs.batch_process(args.input, args.output)
    else:
        # 단일 파일 처리
        result = srs.process_audio_file(args.input, args.method, args.language)
        print(f"\n인식 결과: {result}")
        
        # 결과 파일 저장
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"파일: {args.input}\n")
                f.write(f"결과: {result}\n")
            print(f"결과가 파일에 저장되었습니다: {args.output}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 인터랙티브 모드
        print("=== 음성 파일 인식 시스템 ===")
        srs = SpeechRecognitionSystem()
        
        while True:
            print("\n지원 형식:", ", ".join(srs.supported_formats))
            file_path = input("오디오 파일 경로를 입력하세요 (종료: 'quit'): ").strip()
            
            if file_path.lower() == 'quit':
                break
            
            if not file_path:
                continue
            
            method = input("인식 방법 (google/offline, 기본값: google): ").strip() or 'google'
            language = input("언어 코드 (기본값: ko-KR): ").strip() or 'ko-KR'
            
            result = srs.process_audio_file(file_path, method, language)
            print(f"\n인식 결과: {result}")
    else:
        main()