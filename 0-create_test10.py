import zipfile
import os
import io

# [ClamAV 정상 판정 테스트용 열 번째 파일 생성 스크립트]
# 이 스크립트는 중첩 압축(Nested Zip) 구조를 가지면서도 내부 전부에 무해한 내용만 포함합니다.
# ClamAV가 복잡한 구조 속에서도 정상 파일을 오탐(False Positive)하지 않는지 테스트합니다.

def create_safe_nested_zip():
    """
    이중 압축 구조를 생성하되, 내부에는 어떠한 악성 시그니처도 포함하지 않습니다.
    ClamAV 검사 결과는 'OK'가 나와야 정상입니다.
    """
    try:
        # 파일명 자동 매칭 (0-create_test10.py -> 0-create_test10.zip)
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중 (정상 중첩 압축 구조)...")

        # 인메모리 버퍼에 첫 번째(내부) 정상 ZIP 파일 생성
        inner_zip_buffer = io.BytesIO()
        with zipfile.ZipFile(inner_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as inner_zip:
            # 내부 ZIP에 안전한 텍스트 파일 추가
            inner_zip.writestr("benign_text.txt", "This is a perfectly safe text file inside a nested archive.")
        
        inner_zip_data = inner_zip_buffer.getvalue()

        # 최종(외부) ZIP 파일 생성
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as outer_zip:
            # 안전한 하위 ZIP 파일을 외부 ZIP 안에 추가
            outer_zip.writestr("data/archives/safe_container.zip", inner_zip_data)
            
            # 외부 ZIP에도 정상 문서 파일 추가
            outer_zip.writestr("manifest.txt", "Manifest: No signatures found in this structured archive.")
            
        print(f"✅ 정상 판정용 중첩 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print(f"💡 예상 결과: clamscan {zip_filename}  >>>  OK")
        print("💡 탐지되지 않는 이유:")
        print("  - 내외부 파일 통틀어 악성 시그니처(EICAR 등) 전무")
        print("  - 복잡한 구조를 가졌으나 실제 위해 요소 없음")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    create_safe_nested_zip()
