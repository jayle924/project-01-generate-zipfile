import zipfile
import os

def create_vbs_zip(zip_filename):
    # 1. 시뮬레이션된 VBScript 소스 코드
    # 백신이 주로 탐지하는 '객체 생성' 및 '다운로더' 패턴을 모사합니다.
    vbs_content = """
' 보안 시뮬레이션을 위한 VBScript (교육용)
' 실제 시스템에 어떠한 위해도 가하지 않습니다.

On Error Resume Next
Set objShell = CreateObject("WScript.Shell")

' 시스템 업데이트인 것 처럼 알림 표시
objShell.Popup "환경 설정을 동기화하는 중입니다...", 3, "System Configuration", 64

' 실제 악성코드는 여기에서 인터넷 연결을 시도함
' strDownloadURL = "http://example.com/payload.exe"
' Set objHTTP = CreateObject("MSXML2.XMLHTTP")

' 테스트를 위한 메시지 확인
WScript.Echo "보안 테스트용 스크립트가 로드되었습니다."
"""
    
    print(f"보안 테스트용 [{zip_filename}] 생성 중 (VBScript 기법 적용)...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # .vbs 확장자는 윈도우에서 기본적으로 실행 가능하여 위협 탐지율이 높습니다.
            zf.writestr("Environment_Sync.vbs", vbs_content)
            
        print(f"✅ 성공: '{zip_filename}' 파일이 생성되었습니다.")
        print("💡 특징: VBScript의 CreateObject 패턴을 활용하여 휴리스틱 탐지를 테스트합니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 생성할 압축 파일의 이름 설정
    target_zip = "vbs_test_sample.zip"
    create_vbs_zip(target_zip)
