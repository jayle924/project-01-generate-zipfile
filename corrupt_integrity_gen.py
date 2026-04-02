# 3. 무결성 오류 (CRC-32 Error) 소스 코드
# ZIP 구조는 유지하되 내부 데이터를 임의로 오염시켜 무결성 검증 실패를 유도합니다.

with open("corrupt_integrity.zip", "wb") as f:
    f.write(b"PK\x03\x04" + b"\xFF" * 10 + b"\x00" * 40 + b"Integrity error simulation.")

print("✅ corrupt_integrity.zip 파일이 생성되었습니다. (무결성 오류 방식)")
