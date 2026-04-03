import zipfile
import os

# [ClamAV 정상 판정 테스트용 파일 생성 스크립트 07]
# 이 스크립트는 백신 시그니처나 의심스러운 행위 패턴이 전혀 없는 '정상적인' 파일을 생성합니다.

def create_safe_test_zip_v7():
    """
    백신 탐지에서 제외될 수 있도록 안전한 데이터와 표준 코드를 사용하여 ZIP 파일을 생성합니다.
    ClamAV 검사 시 결과값은 반드시 'OK'가 나옵니다.
    """
    try:
        # 파일명 자동 매칭 (create_test07_zip.py -> create_test07_zip.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        # 1. 안전한 비즈니스 문서 내용
        # - 어떠한 백신 엔진에도 등록되지 않은 무해한 일반 영문 텍스트입니다.
        SAFE_DOC_CONTENT = "Security Final Report: The integration test was successful. All protocols are within safe parameters."

        # 2. 무해한 유틸리티 코드 내용
        # - 시스템 파일을 수정하거나 네트워크 연결을 시도하는 위험 함수가 배제된 표준 코드입니다.
        SAFE_UTILS_CODE = r'''
def format_data(data):
    """입력받은 데이터를 대문자로 변환하는 간단한 유틸리티입니다."""
    return data.upper()

if __name__ == "__main__":
    test_data = "clamav_test_safe"
    print(format_data(test_data))
'''

        # ZIP 파일 생성 (메모리 직접 쓰기 방식 사용)
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 텍스트 문서 추가 (시그니처 누락 테스트)
            zipf.writestr("report.txt", SAFE_DOC_CONTENT.encode('utf-8'))
            
            # 파이썬 유틸리티 파일 추가 (행위 기반 탐지 제외 테스트)
            zipf.writestr("data_utils.py", SAFE_UTILS_CODE.encode('utf-8'))
            
        print(f"✅ 정상 파일용 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지되지 않는 이유:")
        print("  - 등록된 악성 시그니처(EICAR 등) 없음")
        print("  - 자동 실행이나 외부 다운로드 등 위협 패턴 없음")
        print("  - 표준 압축 구조 준수")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    create_safe_test_zip_v7()
