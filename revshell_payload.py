import zipfile
import os

def create_revshell_zip(zip_filename):
    # 1. 시뮬레이션된 리버스 쉘 코드 내용 (Python)
    # 공격자의 C2 서버에 연결을 시도하는 전형적인 백도어 패턴입니다.
    py_content = """
import socket
import os

# 보안 분석 장비 테스트를 위한 시뮬레이션 패킷 송출 스크립트
# 본 코드는 실제 악의적인 행위를 포함하지 않으며 연결 테스트만 수행합니다.

def simulated_backdoor():
    # 일반적인 C2 테스트용 로컬 주소와 포트
    REMOTE_HOST = '127.0.0.1' 
    REMOTE_PORT = 4444
    
    print(f"[*] Attempting simulation connection to {REMOTE_HOST}:{REMOTE_PORT}...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 실제 연결은 안전을 위해 시도하지 않거나 짧은 타임아웃을 둡니다.
        s.settimeout(2)
        # s.connect((REMOTE_HOST, REMOTE_PORT)) 
        print("[+] Connection signature generated.")
    except Exception as e:
        print(f"[-] Connection log generated with error: {e}")

if __name__ == "__main__":
    simulated_backdoor()
"""
    
    print(f"보안 테스트용 [{zip_filename}] 생성 중 (리버스 쉘 패턴)...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # 파이썬 파일을 통해 네트워크 위협 탐지를 유도합니다.
            zf.writestr("network_agent.py", py_content)
            
        print(f"✅ 성공: '{zip_filename}' 파일이 생성되었습니다.")
        print("💡 특징: C2 서버 통신 시나리오를 통한 네트워크 보안 장비 테스트에 적합합니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 생성할 압축 파일의 이름 설정
    target_zip = "revshell_test_sample.zip"
    create_revshell_zip(target_zip)
