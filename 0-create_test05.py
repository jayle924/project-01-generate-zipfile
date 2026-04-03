import zipfile
import os
import base64

# [INFO] 이 스크립트는 100% 탐지되는 EICAR 서명을 포함하지 않습니다.
# 대신 GTUBE(스팸 서명)와 압축 폭탄(Zip Bomb) 기법을 사용하여 탐지를 유도합니다.

# 1. GTUBE (Generic Test for Unsolicited Bulk Email) 서명
# ClamAV에서 탐지할 수 있는 또 다른 표준 테스트 시그니처입니다.
GTUBE_SIG = r'XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X'

# 2. 난독화된 서명 (백신의 정밀 분석 유도)
# EICAR를 Base64로 감싼 뒤 바이너리를 반전(Reverse)시켜 직접적인 시그니처 매칭을 피합니다.
EICAR_RAW = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
# bytes 객체는 [::-1] 슬라이싱을 사용하여 뒤집어야 합니다.
OBFUSCATED = base64.b64encode(base64.b64encode(EICAR_RAW.encode())[::-1]).decode()

def create_final_heuristic_zip():
    try:
        # 파일명 자동 매칭
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중 (GTUBE + 100MB 압축 폭탄 적용)...")

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 1. GTUBE 테스트 서명 (ASCII 기반)
            zipf.writestr("gtube_test_sig.txt", GTUBE_SIG.encode('ascii'))
            
            # 2. 압축 폭탄 (100MB의 0 데이터)
            # 압축 효율이 극단적으로 높아 Heuristics.Zip.Bomb 탐지를 유도합니다.
            zipf.writestr("huge_data_bomb.dat", b"\0" * (1024 * 1024 * 100))
            
            # 3. 난독화된 레이어 파일
            zipf.writestr("signature_layer.enc", OBFUSCATED.encode())

        print(f"✅ 최종 수정본 생성 완료: {zip_filepath}")
        print("💡 탐지 포인트: GTUBE 서명 + 100MB 압축 폭탄 + 난독화 데이터")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    create_final_heuristic_zip()
