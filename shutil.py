import shutil

# 'my_folder'라는 디렉토리를 'archive'라는 이름의 zip 파일로 압축
shutil.make_archive('archive_name', 'zip', 'path/to/my_folder')