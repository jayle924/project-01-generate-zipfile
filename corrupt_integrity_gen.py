import struct

def create_advanced_corrupt_zip(zip_filename):
    """
    AWS-ClamAV의 휴리스틱 엔진을 가장 강력하게 자극하기 위해
    바이너리 레벨에서 ZIP 구조를 직접 조작하여 생성합니다.
    (Zip-Slip 경로 조작 + 헤더 길이 변조 + 무결성 오류 + EICAR 통합)
    """
    print(f"AWS-ClamAV 휴리스틱 탐지용 [{zip_filename}] 생성 중...")
    
    # 1. ClamAV가 즉각 반응할 수 있는 EICAR 시그니처 준비
    EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
    
    # 2. 의도적으로 조작된 파일명 (Zip-Slip 경로 조작 공격 패턴)
    # 일반적인 라이브러리는 이를 차단하므로 바이너리로 직접 삽입합니다.
    malicious_filename = b"../../../../../../etc/passwd"
    
    try:
        with open(zip_filename, "wb") as f:
            # --- ZIP Local File Header (LFH) 직접 구성 ---
            # Signature (4 bytes): PK\x03\x04
            f.write(b"PK\x03\x04")
            # Version needed to extract (2 bytes): 2.0 (20)
            f.write(struct.pack("<H", 20))
            # General purpose bit flag (2 bytes): 0
            f.write(struct.pack("<H", 0))
            # Compression method (2 bytes): 0 (Stored/No compression)
            f.write(struct.pack("<H", 0))
            # Last mod file time/date (4 bytes): 0
            f.write(struct.pack("<I", 0))
            
            # --- 고의적 데이터 파괴 구역 ---
            # 3. CRC-32 (4 bytes): 의도적으로 틀린 값 삽입 (0xDEADBEEF) -> 무결성(Integrity) 오류 유발
            f.write(struct.pack("<I", 0xDEADBEEF))
            # Compressed size (4 bytes): 데이터 길이
            f.write(struct.pack("<I", len(EICAR_SIG)))
            # Uncompressed size (4 bytes): 데이터 길이
            f.write(struct.pack("<I", len(EICAR_SIG)))
            
            # 4. Filename length (2 bytes)
            f.write(struct.pack("<H", len(malicious_filename)))
            
            # 5. Extra field length (2 bytes): 최대치(0xFFFF) 설정 
            # -> 실제 데이터보다 훨씬 큰 길이를 선언하여 헤더 포맷 오류 및 버퍼 오버플로우 분석 유도
            f.write(struct.pack("<H", 0xFFFF))
            
            # --- 데이터 삽입 ---
            # 6. 조작된 파일명 기록 (Path Traversal 시그니처)
            f.write(malicious_filename)
            
            # 7. 실제 페이로드 기록 (EICAR 바이러스 서명)
            f.write(EICAR_SIG.encode())
            
            # 8. 후속 데이터 채우기 (분석 엔진의 혼란 유도)
            f.write(b"\x00" * 100 + b"DAMAGED_DATA_BLOCK")

        print(f"✅ 생성 완료: {zip_filename}")
        print("💡 적용된 휴리스틱 자극 기법:")
        print("  - Zip-Slip (Path Traversal Detection)")
        print("  - Oversized Extra Field (Header Formatting Error)")
        print("  - Invalid CRC-32 (Integrity Check Failure)")
        print("  - EICAR Signature (Standard Virus Detection)")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    target_name = "corrupt_integrity.zip"
    create_advanced_corrupt_zip(target_name)
