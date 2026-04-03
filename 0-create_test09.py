import zipfile
import os

# [ClamAV 정상 판정 테스트용 파일 생성 스크립트 09]
# 이 스크립트는 백신이 위협 요소를 찾을 수 없는 '정상적인' 파일을 생성합니다.
# 이전 버전의 감염 서명(EICAR)과 리버스 쉘 의심 패턴을 모두 제거했습니다.

def create_safe_test_zip_v9():
    """
    백신 시그니처나 의심스러운 행위 패턴이 없는 표준 ZIP 파일을 생성합니다.
    ClamAV 검사 시 결과값은 반드시 'OK'가 나옵니다.
    """
    try:
        # 파일명 자동 매칭 (create_test09_zip.py -> create_test09_zip.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        # 1. 안전한 유틸리티 설명 내용
        # - 어떠한 백신 엔진에도 등록되지 않은 무해한 일반 영문 텍스트입니다.
        SAFE_TEXT_CONTENT = "File Utility Tool: This document contains usage instructions for the directory listing script."

        # 2. 무해한 관리용 파이썬 코드 내용
        # - 단순 파일 목록 출력 기능만 있으며, 네트워크 연결이나 시스템 수정을 하지 않습니다.
        SAFE_ADMIN_CODE = r'''
import os

def list_workspace_files():
    """현재 작업 폴더의 파일 목록을 출력하는 안전한 함수입니다."""
    current_path = os.getcwd()
    print(f"Listing files in: {current_path}")
    files = [f for f in os.listdir(current_path) if os.path.isfile(f)]
    for file in files:
        print(f" - {file}")

if __name__ == "__main__":
    list_workspace_files()
'''

        # ZIP 파일 생성 (메모리 직접 쓰기 방식 사용)
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 설명 문서 추가
            zipf.writestr("utility_readme.txt", SAFE_TEXT_CONTENT.encode('utf-8'))
            
            # 파이썬 관리 툴 추가
            zipf.writestr("file_lister.py", SAFE_ADMIN_CODE.encode('utf-8'))
            
        print(f"✅ 정상 파일용 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지되지 않는 이유:")
        print("  - 감염 서명(EICAR, GTUBE 등) 전혀 없음")
        print("  - 리버스 쉘이나 드롭퍼 등 악성 행위 패턴 제거됨")
        print("  - 표준 라이브러리 기반의 안전한 코드 구조")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    create_safe_test_zip_v9()
