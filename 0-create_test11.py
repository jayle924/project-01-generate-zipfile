import zipfile
import os

# [ClamAV 탐지 우회(Bypass) 테스트용 열한 번째 파일]
# 바이러스 시그니처(EICAR)를 내포하고 있지만, 백신이 탐지하지 못하게 만드는 기법을 테스트합니다.
# 시그니처 기반 백신은 '특정 패턴이 연속적으로' 나타나야 탐지한다는 점을 이용합니다.

# 1. 원본 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_stealth_infection_zip():
    """
    서명을 파편화(Fragmentation)하여 ZIP 파일에 저장함으로써 ClamAV의 탐지를 우회합니다.
    시그니처는 존재하지만, 연속성이 깨졌기 때문에 결과는 'OK'가 나옵니다.
    """
    try:
        # 파일명 자동 매칭 (0-create_test11.py -> 0-create_test11.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중 (시그니처 파편화 우회 기법 적용)...")

        # 시그니처 조각내기 (절반으로 분리)
        # 백신 엔진은 이 조각들을 각각의 파일로 볼 때 악성으로 판단하지 않습니다.
        half = len(EICAR_SIG) // 2
        sig_part1 = EICAR_SIG[:half]
        sig_part2 = EICAR_SIG[half:]

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 첫 번째 조각 저장
            zipf.writestr("data_vol1.bin", sig_part1.encode('ascii'))
            
            # 두 번째 조각 저장
            zipf.writestr("data_vol2.bin", sig_part2.encode('ascii'))
            
            # 우회 성공 메시지 (설명용)
            zipf.writestr("note.txt", "The EICAR signature is split between vol1 and vol2. ClamAV will say OK.")

        print(f"✅ 우회 성공용 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지 우회 원리:")
        print(f"  - 바이러스 서명({len(EICAR_SIG)}바이트)이 연속되지 않고 두 파일로 나뉨")
        print("  - 백신의 '패턴 매칭' 엔진은 조각난 서명을 인식하지 못함")
        print("  - 실제 공격자가 탐지를 피하기 위해 사용하는 원시적인 방법 중 하나임")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 에러 발생: {e}")

if __name__ == "__main__":
    create_stealth_infection_zip()
