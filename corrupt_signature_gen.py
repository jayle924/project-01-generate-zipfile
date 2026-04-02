# 1. 헤더 변조 (Invalid Signature) 소스 코드
# ZIP 파일의 시작 식별자인 'PK'를 'XX'로 변경하여 포맷 오류를 유도합니다.

with open("corrupt_signature.zip", "wb") as f:
    f.write(b"XX\x03\x04" + b"\x00" * 20 + b"Broken Header Simulation")

print("✅ corrupt_signature.zip 파일이 생성되었습니다. (헤더 변조 방식)")
