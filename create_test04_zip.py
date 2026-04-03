import zipfile
import os

# 1. 100% 탐지 보장을 위한 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# 2. 배치(Batch) 스크립트에서의 레지스트리 수정 패턴입니다.
# - REG ADD: 레지스트리에 새로운 키나 값을 추가합니다.
# - CurrentVersion\Run: 윈도우 시작 시 자동 실행되는 프로그램 목록으로, 악성코드가 상주하는 단골 위치입니다.
# - 이러한 시스템 설정 변경 시도는 백신의 휴리스틱 엔진에 의해 즉시 차단되거나 경고를 받게 됩니다.
BATCH_SUSPICIOUS = r'''
@echo off
REM ClamAV Registry Persistence Test Script (Batch Mock)
REM ----------------------------------------------------
REM [HEURISTIC] 시스템 시작 시 자동 실행을 위한 레지스트리 등록 시도:
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "MyInfectedTest" /t REG_SZ /d "C:\temp\malicious.exe" /f

echo Security test key added to Registry...
'''

def create_guaranteed_test_zip():
    """
    네 번째 테스트 세트로, 배치 파일 기반의 시스템 설정 변경 패턴과 고정 서명을 포함합니다.
    파일 관리 편의를 위해 스크립트 파일명을 따라 ZIP 파일명이 결정됩니다.
    """
    try:
        # 현재 실행 중인 스크립트 파일명 기반으로 ZIP 명칭 결정
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        # 저장 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 시그니처: 무조건 탐지되는 EICAR 서명 파일
            zipf.writestr("signature/eicar_core.txt", EICAR_SIG.encode('ascii'))
            
            # 행위: 배치 스크립트 의심 패턴 파일
            zipf.writestr("payload/persistence.bat", BATCH_SUSPICIOUS.encode('utf-8'))
            
        print(f"✅ 생성 완료: {zip_filepath}")
        print(f"📦 생성된 ZIP: {zip_filename}")
        print("💡 탐지 포인트: Batch Registry Modification + EICAR 서명 복합")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    create_guaranteed_test_zip()
