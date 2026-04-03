import zipfile
import os

# [ClamAV 탐지 우회(Bypass) 테스트용 열 번째 파일]
# 이번에는 시그니처 'XOR 암호화(XOR Encryption)' 기법을 사용하여 ClamAV를 우회합니다.
# 실제 악성코드가 백신의 탐지를 피하기 위해 가장 많이 사용하는 입문적인 암호화 방식입니다.

# 1. 원본 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_xor_stealth_zip():
    """
    서명을 특정 키로 XOR 연산하여 저장함으로써 ClamAV의 탐지를 우회합니다.
    시그니처가 존재하지만 바이너리 형태가 변조되었으므로 결과는 'OK'가 나옵니다.
    """
    try:
        # 파일명 자동 매칭 (0-create_test10.py -> 0-create_test10.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중 (시그니처 XOR 연산 우회 기법 적용)...")

        # 시그니처를 XOR 연산 처리 (Key: 0x42)
        # 각 바이트를 키값과 XOR 하면 원래의 패턴이 완전히 깨지게 됩니다.
        xor_key = 0x42
        xor_payload = bytes([b ^ xor_key for b in EICAR_SIG.encode('ascii')])

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # XOR 처리된 바이너리 페이로드 파일 추가
            zipf.writestr("xor_encrypted.bin", xor_payload)
            
            # 우회 성공 메시지 (설명용)
            zipf.writestr("bypass_info.txt", f"The EICAR signature is XORed with key {hex(xor_key)}. ClamAV will say OK.")

        print(f"✅ 우회 성공용 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지 우회 원리:")
        print("  - 시그니처의 모든 비트를 특정 키로 반전시켜 패턴 매칭을 무력화함")
        print("  - 암호화된 상태에서는 그 어떤 백신도 서명을 인식하지 못함")
        print("  - 실제 공격 시에는 이 데이터를 디코딩하는 짧은 코드가 앞단에 붙습니다.")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 에러 발생: {e}")

if __name__ == "__main__":
    create_xor_stealth_zip()
