import zipfile
import os

# EICAR (European Institute for Computer Antivirus Research) 표준 안티바이러스 테스트 파일 문자열입니다.
# 1. 탐지 이유: 이 68바이트 문자열은 전 세계 모든 백신 소프트웨어(ClamAV 포함)가 
#    '바이러스'로 인식하도록 사전에 정의된 표준 시그니처입니다. 
# 2. 실제 위험성: 실제 악성 코드가 아니며, 단순히 백신의 탐지 및 차단 기능을 테스트하기 위한 용도입니다.
# 3. ZIP 파일 탐지: ClamAV는 압축 파일 내부를 검색하는 엔진을 포함하고 있어, 
#    ZIP 안에 있는 이 문자열을 찾아내어 감염된 파일로 보고합니다.
EICAR_STRING = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

def create_clamav_test_zip(zip_filepath, inner_filename="eicar_test.txt"):
    """
    임시 파일을 디스크에 생성하지 않고 메모리에서 직접 ZIP 내부로 데이터를 기록합니다.
    이 방식은 Windows Defender와 같은 백신이 중간 임시 파일을 삭제하여 생기는 OSError를 방지합니다.
    """
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # writestr: 디스크에 파일을 쓰지 않고 바로 압축 파일 내부에 데이터 기록
            zipf.writestr(inner_filename, EICAR_STRING.encode('ascii'))
        print(f"성공적으로 생성됨: {zip_filepath}")
        print(f"내부 포함 파일: {inner_filename}")
    except Exception as e:
        print(f"파일 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    # 스크립트 위치 기준 절대 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_zip = os.path.join(current_dir, "clamav_test_eicar.zip")
    
    # 실행
    create_clamav_test_zip(target_zip, "eicar_test.txt")
