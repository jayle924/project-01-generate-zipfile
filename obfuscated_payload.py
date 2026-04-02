import zipfile
import base64
import os

# 1. 원본 페이로드 (EICAR 테스트 문자열)
raw_payload = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# 2. 페이로드를 Base64로 인코딩 (백신을 속이기 위한 기초적인 난독화)
encoded_payload = base64.b64encode(raw_payload.encode()).decode()

def create_obfuscated_zip(zip_filename):
    # 3. 인코딩된 데이터를 복호화해서 실행하는 '실행기(Launcher)' 스크립트 작성
    # 실제 악성코드가 실행 시점에 데이터를 복호화하는 방식을 모사함
    launcher_script = f"""
# 보안 테스트를 위한 시뮬레이션된 난독화 페이로드
# 본 스크립트는 교육 및 보안 점검 목적으로 작성되었습니다.

$data = "{encoded_payload}"
$decoded = [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String($data))

Write-Host "--- Simulated Payload Decoder ---"
Write-Host "Encoded Data: $data"
Write-Host "Decoded Result: $decoded"
Write-Host "---------------------------------"
"""
    
    print(f"보안 테스트용 [{zip_filename}] 생성 중 (난독화 기범 적용)...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # 파워쉘 스크립트 형태로 압축 파일 내부에 저장
            zf.writestr("launcher.ps1", launcher_script)
            
        print(f"✅ 생성 완료: {zip_filename}")
        print("💡 특징: 페이로드가 Base64로 인코딩되어 'launcher.ps1' 내부에 숨겨져 있습니다.")
        print("이 방식은 백신의 동적 분석 및 휴리스틱 탐지 기능을 테스트하기에 적합합니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 압축 파일 이름 설정
    target_zip = "obfuscated_test_sample.zip"
    create_obfuscated_zip(target_zip)
