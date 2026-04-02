import zipfile
import io

#감염된 압축 파일을 메모리에 생성
def create_infected_zip_in_memory(zip_name, infected_file_name):
    # EICAR 테스트 문자열
    eicar_string = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

    try:
        # 파일을 디스크에 쓰지 않고 메모리(BytesIO)에서 직접 작업
        with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # writestr을 사용하면 실제 파일을 만들지 않고 내용만 압축 안에 넣습니다.
            zf.writestr(infected_file_name, eicar_string)
            
        print(f"[*] 성공: {zip_name} 파일이 생성되었습니다.")
        print(f"[*] 이제 이 파일을 S3에 업로드해서 람다 테스트를 진행하세요.")

    except Exception as e:
        print(f"[!] 에러 발생: {e}")

if __name__ == "__main__":
    # 백신을 속이기 위해 파일명을 아주 평범하게 정합니다.
    create_infected_zip_in_memory("infected_test.zip", "normal_data.txt")