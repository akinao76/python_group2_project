import ftplib
import os

def ftpdir(ip_addr, login_id, login_pw, filename): 
    ftp = ftplib.FTP(ip_addr)
    ftp.login(login_id, login_pw)

    #프로젝트 이름 추출 (예: projectX_report.txt → projectX)
    project_name = filename.split('_')[0]

    if project_name not in ftp.nlst():
        ftp.mkd(project_name)

    ftp.cwd(project_name)

    with open(filename, 'rb') as f:
        ftp.storbinary(f'STOR {os.path.basename(filename)}', f)

    print(f"{filename} 파일을 FTP 서버의 /{project_name}/ 폴더에 업로드했습니다.")

    ftp.quit()

# 매직 넘버와 파일 형식을 매칭
MAGIC_NUMBERS = {
    b'\x25\x50\x44\x46': 'PDF file',
    b'\x50\x4B\x03\x04': 'DOCX/XLSX file',
    b'\xFF\xD8\xFF\xE0': 'JPEG image file',
    b'\x89\x50\x4E\x47': 'PNG image file',
}

# 상대 경로 사용
DIR_PATH = './'  # 현재 작업 디렉토리 기준으로 사용

# 파일의 매직 넘버를 검사하는 함수
def check_file_magic_number(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        file_header = file.read(4)  # 첫 4바이트를 읽어서 매직 넘버 검사

    # 매직 넘버 검사
    for magic, file_type in MAGIC_NUMBERS.items():
        if file_header.startswith(magic):
            return f"{file_name} is a {file_type}"

    return f"{file_name}: File type not recognized"

# 지정된 디렉토리 내 모든 파일 검사
def check_directory_files(directory_path):
    results = []

    # 디렉토리 내 모든 파일 검사 (for문 사용)
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        
        # 파일만 검사
        if os.path.isfile(file_path):  # 파일만 검사
            print(f"Checking file: {file_path}")  # 디버깅을 위한 출력
            result = check_file_magic_number(file_path)
            results.append(result)

    return results

# 결과 출력
results = check_directory_files(DIR_PATH)
for result in results:
    print(result)
