import zipfile
import os

# infected_zip.py 파일을 실행하면 감염 테스트용 압축 파일을 생성합니
def create_infected_zip(zip_name, infected_file_name):
    # 1. EICAR 테스트 표준 문자열 (백신 엔진이 바이러스로 인식함)
    # 이 문자열은 실제 바이러스가 아니라 표준화된 테스트용 텍스트입니다.
    eicar_string = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

    # 2. 가짜 감염 파일 생성
    with open(infected_file_name, 'w') as f:
        f.write(eicar_string)
    
    # 3. 압축 파일 생성 및 가짜 감염 파일 추가
    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(infected_file_name)
        
    # 생성 후 원본 텍스트 파일은 삭제 (깔끔하게 관리)
    if os.path.exists(infected_file_name):
        os.remove(infected_file_name)

    print(f"[*] 감염 테스트용 압축 파일 생성 완료: {zip_name}")
    print(f"[!] 주의: 백신이 실시간 감시 중이라면 이 파일을 즉시 삭제하거나 경고를 띄울 수 있습니다.")

if __name__ == "__main__":
    target_zip = "infected_test.zip"
    virus_sample = "eicar_virus.txt"
    
    create_infected_zip(target_zip, virus_sample)
    