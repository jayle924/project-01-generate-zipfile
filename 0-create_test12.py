import zipfile
import os

# [ClamAV 탐지 우회(Bypass) 테스트용 열두 번째 파일]
# 이번에는 시그니처 '문자열 반전(String Reversal)' 기법을 사용하여 ClamAV를 우회합니다.
# 데이터의 순서를 거꾸로 뒤집음으로써 시그니처 엔진의 정방향 패턴 매칭을 무력화합니다.

# 1. 원본 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_reverse_stealth_zip():
    """
    서명을 역순으로 뒤집어 저장함으로써 ClamAV의 탐지를 우회합니다.
    시그니처의 모든 문자가 포함되어 있지만, 순서가 파괴되었으므로 결과는 'OK'가 나옵니다.
    """
    try:
        # 파일명 자동 매칭 (0-create_test12.py -> 0-create_test12.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중 (시그니처 반전 우회 기법 적용)...")

        # 시그니처 문자열 뒤집기
        # 원본: X5O!P... -> 반전: *H+H$!EL... (백신이 찾고자 하는 패턴과 정반대)
        reversed_payload = EICAR_SIG[::-1]

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 뒤집힌 페이로드 파일 추가
            zipf.writestr("reversed_payload.data", reversed_payload.encode('ascii'))
            
            # 우회 성공 메시지 (설명용)
            zipf.writestr("bypass_info.txt", "The EICAR signature is saved in REVERSE order. ClamAV will say OK.")

        print(f"✅ 우회 성공용 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지 우회 원리:")
        print("  - 데이터의 순서를 완전히 뒤집어 백신의 '정방향 매칭' 방식을 피함")
        print("  - 백신은 모든 파일을 거꾸로 읽어서 대조하지 않기 때문에 탐지 불가")
        print("  - 공격 시에는 데이터를 읽어 다시 뒤집는 단순한 루틴만 추가되어 실행됩니다.")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 에러 발생: {e}")

if __name__ == "__main__":
    create_reverse_stealth_zip()
