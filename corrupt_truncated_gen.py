# 2. 데이터 절단 (Truncated/Incomplete) 소스 코드
# ZIP 파일의 필수 구조인 Central Directory를 누락시켜 데이터가 잘린 상태를 모사합니다.

with open("corrupt_truncated.zip", "wb") as f:
    f.write(b"PK\x03\x04\x14\x00\x00\x00\x00\x00" + b"Truncated data sequence...")

print("✅ corrupt_truncated.zip 파일이 생성되었습니다. (데이터 절단 방식)")
