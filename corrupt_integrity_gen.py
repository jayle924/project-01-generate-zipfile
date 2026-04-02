import struct

import struct

def create_advanced_corrupt_zip(zip_filename):
    """
    AWS-ClamAV(S3-Antivirus Lambda)의 탐지를 극대화하기 위해 
    파일 전방 시그니처 주입, 압축 폭탄 헤더, 파일 중첩 및 후방 오버레이를 통합합니다.
    """
    print(f"AWS-ClamAV 최적화 탐지용 [{zip_filename}] 생성 중...")
    
    # 표준 안티바이러스 테스트 시그니처
    EICAR_SIG = b'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
    
    try:
        with open(zip_filename, "wb") as f:
            # 1. 전방 주입 (Prefix Injection)
            # ClamAV가 압축 해제를 시도하기 전에 파일 전두부에서 즉각 탐지하도록 함
            f.write(EICAR_SIG + b"\n")
            
            # --- ZIP Local File Header (LFH) 시작 ---
            lfh_start = f.tell()
            f.write(b"PK\x03\x04")
            f.write(struct.pack("<H", 20)) # Version
            f.write(struct.pack("<H", 0))  # Flags
            f.write(struct.pack("<H", 0))  # Method: Stored
            f.write(struct.pack("<I", 0))  # Time/Date
            
            # 2. 압축 폭탄 (Zip Bomb) 시뮬레이션
            # Uncompressed size를 최대치(4GB)로 설정하여 Heuristics.Zip.Bomb 유도
            f.write(struct.pack("<I", 0xDEADBEEF)) # Bad CRC
            f.write(struct.pack("<I", len(EICAR_SIG))) # Compressed size
            f.write(struct.pack("<I", 0xFFFFFFFF))      # Uncompressed size (Fake 4GB)
            
            # 3. Zip-Slip + 긴 경로 (Path Traversal)
            malicious_path = b"../../../../" * 10 + b"etc/shadow"
            f.write(struct.pack("<H", len(malicious_path)))
            f.write(struct.pack("<H", 0x0000)) # Extra field length
            f.write(malicious_path)
            
            # 데이터 영역 (EICAR 페이로드)
            f.write(EICAR_SIG)
            
            # 4. 중첩/오버랩 (Overlapping Headers) 시뮬레이션
            # 두 번째 LFH를 바로 뒤에 붙여 구조적 모순 발생시킴
            f.write(b"PK\x03\x04")
            f.write(b"\x00" * 26) # Dummy header
            
            # --- Central Directory Record 시뮬레이션 ---
            cd_start = f.tell()
            f.write(b"PK\x01\x02")
            f.write(b"\x00" * 42) # Dummy CD
            
            # End of Central Directory
            eocd_start = f.tell()
            f.write(b"PK\x05\x06")
            f.write(b"\x00" * 18) # Dummy EoCD
            
            # 5. 후방 오버레이 (Trailing Data)
            # EoCD 이후에 악성 시그니처를 추가하여 Heuristics.Zip.TrailingData 유도
            f.write(b"\n" + EICAR_SIG)
            f.write(b"\nMALICIOUS_OVERLAY_DATA")

        print(f"✅ 생성 완료: {zip_filename}")
        print("💡 적용된 AWS-ClamAV 탐지 강화 기법:")
        print("  - 파일 전두부 EICAR 시그니처 주입 (즉각 탐지)")
        print("  - 압축 폭탄 헤더 (4GB 선언으로 스캔 엔진 무력화 테스트)")
        print("  - Zip-Slip (Deep Path Traversal 시그니처)")
        print("  - 파일 구조 중첩 및 무결성 파괴")
        print("  - 파일 후방 오버레이 데이터(EICAR) 추가")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    target_name = "corrupt_integrity.zip"
    create_advanced_corrupt_zip(target_name)
