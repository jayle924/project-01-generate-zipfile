# 3. 무결성 오류 (CRC-32 Error) + AWS-ClamAV 탐지 최적화
# ZIP 구조는 유지하되 내부 데이터를 오염시키고,
# ClamAV가 즉각 반응할 수 있는 EICAR 시그니처를 포함합니다.

# ClamAV가 감지할 수 있는 표준 안티바이러스 테스트 파일 문자열
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_clamav_corrupt_zip():
    print("AWS-ClamAV 탐지용 손상 파일(Integrity Error) 생성 중...")
    
    with open("corrupt_integrity.zip", "wb") as f:
        # 1. ZIP 로컬 파일 헤더 시뮬레이션 (PK\x03\x04)
        f.write(b"PK\x03\x04\x14\x00\x00\x00\x08\x00") 
        
        # 2. 데이터 영역에 EICAR 시그니처를 직접 삽입 (탐지 유연성 확보)
        # 이 문자열이 파일 원본 바이트에 포함되면 ClamAV는 즉각 반응합니다.
        f.write(EICAR_SIG.encode())
        
        # 3. 강제로 데이터를 오염시켜 무결성(CRC) 오류 유발
        # 시그니처 뒤에 의미 없는 바이트들을 대량 추가하여 정상적인 압축 해제를 방해합니다.
        f.write(b"\xFF" * 200 + b"\x00" * 200 + b"DAMAGED_INTEGRITY_DATA")

    print("✅ 성공: corrupt_integrity.zip 파일이 생성되었습니다.")
    print("💡 특징: 압축 구조 손상과 바이러스 시그니처를 결합하여 탐지율을 극대화했습니다.")

if __name__ == "__main__":
    create_clamav_corrupt_zip()
