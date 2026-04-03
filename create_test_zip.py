import zipfile
import os

# EICAR (European Institute for Computer Antivirus Research) 표준 안티바이러스 테스트 파일 문자열입니다.
# 1. 탐지 이유: 이 68바이트 문자열은 전 세계 모든 백신 소프트웨어(ClamAV 포함)가 
#    '바이러스'로 인식하도록 사전에 정의된 표준 시그니처입니다. 
# 2. 실제 위험성: 실제 악성 코드가 아니며, 단순히 백신의 탐지 및 차단 기능을 테스트하기 위한 용도입니다.
# 3. ZIP 파일 탐지: ClamAV는 압축 파일 내부를 검색하는 엔진을 포함하고 있어, 
#    ZIP 안에 있는 이 문자열을 찾아내어 감염된 파일로 보고합니다.
EICAR_STRING = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_clamav_test_zip(zip_filename, inner_filename="eicar_test.txt"):
    """
    EICAR 테스트 문자열을 포함한 ZIP 파일을 생성합니다.
    ClamAV는 이 파일을 'Eicar-Test-Signature' 등으로 탐지하게 됩니다.
    """
    # 1. EICAR 문자열을 가진 임시 텍스트 파일 생성
    with open(inner_filename, "w") as f:
        f.write(EICAR_STRING)
    
    # 2. ZIP 파일로 압축 (ClamAV는 압축 해제 후 내부 시그니처를 검사함)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(inner_filename)
        
    # 3. 임시 파일 삭제
    os.remove(inner_filename)
    print(f"성공적으로 생성됨: {zip_filename}")

if __name__ == "__main__":
    # 스크립트 파일이 위치한 디렉토리 절대 경로를 가져옵니다.
    # 이렇게 하면 어느 디렉토리에서 실행하든 스크립트와 같은 곳에 파일이 생깁니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 생성될 파일 경로를 절대 경로로 설정
    target_zip = os.path.join(current_dir, "clamav_test_eicar.zip")
    
    # 임시 파일도 같은 폴더 내에 생성되도록 설정
    temp_inner_file = os.path.join(current_dir, "eicar_test.txt")
    
    create_clamav_test_zip(target_zip, temp_inner_file)
