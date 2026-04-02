import os

# 파일 이름을 'corrupted_test.zip'으로 정해서 하나만 생성합니다.
file_name = "corrupted_test.zip"

with open(file_name, "wb") as f:
    # ZIP 파일의 형식을 완전히 무시하고 가짜 데이터를 넣습니다.
    f.write(b"CORRUPTED_ZIP_DATA_TEST_BY_SOHEE_2026")

print(f"✅ '{file_name}' 파일이 생성되었습니다. 이제 S3에 업로드해 보세요!")