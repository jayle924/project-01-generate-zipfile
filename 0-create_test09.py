import zipfile
import os
import base64

# [ClamAV 탐지 우회(Bypass) 테스트용 아홉 번째 파일]
# 이번에는 시그니처 '인코딩(Encoding)' 기법을 사용하여 ClamAV를 우회합니다.
# 바이러스 서명을 다른 진법(Base64)으로 변환하여 저장함으로써 백신이 바로 알아보지 못하게 만듭니다.

# 1. 원본 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_encoded_stealth_zip():
    """
    서명을 Base64로 인코딩하여 저장함으로써 ClamAV의 탐지를 우회합니다.
    데이터 내부에 서명이 존재하지만, '형태'가 바뀌었기 때문에 결과는 'OK'가 나옵니다.
    """
    try:
        # 파일명 자동 매칭 (0-create_test09.py -> 0-create_test09.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중 (시그니처 인코딩 우회 기법 적용)...")

        # 시그니처를 Base64로 인코딩 (원본과 완전히 다른 문자열 생성)
        # 백신의 시그니처 엔진은 'EICAR...'라는 시작 문구를 찾는데, 인코딩된 데이터는 이를 포함하지 않습니다.
        encoded_payload = base64.b64encode(EICAR_SIG.encode('ascii')).decode()

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 인코딩된 페이로드 파일 추가
            zipf.writestr("hidden_payload.enc", encoded_payload)
            
            # 우회 성공 메시지 (설명용)
            zipf.writestr("bypass_info.txt", "The EICAR signature is Base64 encoded inside the .enc file. ClamAV will say OK.")

        print(f"✅ 우회 성공용 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지 우회 원리:")
        print("  - 시그니처를 Base64로 인코딩하여 백신의 패턴 매칭 엔진을 피함")
        print("  - 백신의 '자동 해독' 기능이 작동하지 않는 일반 텍스트 포맷 사용")
        print("  - 실제 위기 시에는 이 데이터를 디코딩하여 악성 행위를 수행하는 코드가 조합됩니다.")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 에러 발생: {e}")

if __name__ == "__main__":
    create_encoded_stealth_zip()
