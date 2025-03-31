import ftplib
import os

#파일을 폴더별로 분류하는 함수
def ftpdir(ip_addr, login_id, login_pw, filename): 
    ftp = ftplib.FTP(ip_addr)
    ftp.login(login_id, login_pw)

    #프로젝트 이름 추출 (예: projectX_report.txt → projectX)
    project_name = filename.split('_')[0]

    #만약 폴더가 존재하지 않는다면 폴더 이름 만들기
    if project_name not in ftp.nlst():
        ftp.mkd(project_name)

    ftp.cwd(project_name)

    #폴더 저장하기
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
    b'\x4D\x5A': 'EXE file',
}

DIR_PATH = './'  # 현재 작업 디렉토리 기준

# 매직 넘버 검사
def check_magic_number(file_path):
    with open(file_path, 'rb') as file:
        file_header = file.read(4)  # 첫 4바이트 읽기

    for magic, file_type in MAGIC_NUMBERS.items():
        if file_header.startswith(magic):
            return file_type  # 파일 타입 반환
    return None  # 매직넘버가 없으면 None 반환

# 파일이 진짜 텍스트 파일인지 확인하는 함수
def is_text_file(file_path):
    # 1. 매직넘버 검사 → 바이너리 파일이면 바로 False 반환
    detected_type = check_magic_number(file_path)
    if detected_type:
        return False  # txt로 위장한 바이너리 파일 차단

    # 2. 확장자가 .txt인지 확인
    if not file_path.lower().endswith('.txt'):
        return False  

    # 3. UTF-8로 읽을 수 있는지 확인
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read(1000)  # 앞부분 1000자만 확인
    except UnicodeDecodeError:
        return False

    # 4. 바이너리 패턴 검사 (NULL 문자 포함 여부 등)
    if '\x00' in content:  # NULL 문자가 있으면 바이너리 파일로 간주
        return False  

    return True  # 모든 검사를 통과하면 텍스트 파일로 인정

# 파일 검사
def check_file(file_path):
    file_name = os.path.basename(file_path)
    
    if is_text_file(file_path):
        return f"{file_name} is a TXT file (UTF-8)"
    
    return f"{file_name}: File type not recognized"

# 지정된 디렉토리 내 모든 파일 검사
def check_directory_files(directory_path):
    results = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        
        if os.path.isfile(file_path):
            print(f"Checking file: {file_path}")  # 디버깅을 위한 출력
            result = check_file(file_path)
            results.append(result)

    return results

# 결과 출력
results = check_directory_files(DIR_PATH)
for result in results:
    print(result)