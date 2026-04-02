import zipfile
import os

# 1. EICAR 표준 안티바이러스 테스트 문자열 (안전한 테스트용)
# 이 문자열은 전 세계 모든 백신 소프트웨어가 탐지 테스트를 위해 악성 코드로 인식하도록 약속된 문자열입니다.
EICAR_STRING = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_simulated_infected_zip(zip_filename, inner_filename):
    """
    보안 시스템(백신, 샌드박스 등)의 탐지 기능을 테스트하기 위해 
    가짜 감염 파일을 포함한 압축 파일을 생성합니다.
    """
    print(f"보안 테스트용 [{zip_filename}] 생성 중...")
    
    try:
        # 압축 파일 생성
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # 압축 파일 내부에 EICAR 테스트 문자열을 가진 파일 추가
            zf.writestr(inner_filename, EICAR_STRING)
            
        print(f"✅ 성공: '{zip_filename}' 파일이 생성되었습니다.")
        print(f"내부 페이로드 파일명: {inner_filename}")
        print("\n[알림] 백신이 활성화되어 있다면 실시간 감시 기능에 의해 바로 탐지/삭제될 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 설정: 압축 파일 이름과 내부의 '감염된 척하는' 파일 이름
    target_zip = "simulated_infected.zip"
    payload_file = "test_payload.com" # .com 확장자는 탐지 테스트에 효과적입니다.
    
    create_simulated_infected_zip(target_zip, payload_file)
