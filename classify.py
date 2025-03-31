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
    b'\x25\x50\x44\x46': 'PDF file',  # %PDF
    b'\x50\x4B\x03\x04': ' DOCX/XLSX file',  # ZIP, DOCX, XLSX (모두 ZIP 형식)
    b'\xFF\xD8\xFF': 'JPEG image file',  # JPG
    b'\x89\x50\x4E\x47': 'PNG image file',  # PNG
    b'\x4D\x5A': 'EXE file',  # EXE 파일의 매직 넘버 (MZ)
}

DIR_PATH = './'  # 현재 디렉토리 기준

# 파일 매직 넘버 검사
def check_magic_number(file_path):
    with open(file_path, 'rb') as file:
        file_header = file.read(4)  # 앞 4바이트만 읽음

    for magic, file_type in MAGIC_NUMBERS.items():
        if file_header.startswith(magic):
            return file_type  # 파일 타입 반환
    return None  # 매직 넘버가 없으면 None 반환

# 텍스트 파일인지 검사
def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()  # 파일 전체 내용 읽기
        return True
    except UnicodeDecodeError:
        return False

# 파일 검사 함수
def check_file(file_path):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1].lower()

    # 매직 넘버 검사 (EXE 파일은 .txt 확장자라도 인식)
    if file_extension == '.txt'or file_extension == '.exe':
        detected_type = check_magic_number(file_path)
        
        if detected_type == 'EXE file':  # EXE 파일로 판별되면
            return f"{file_name}: File type not recognized"
        
        # 정상적인 텍스트 파일인지 확인
        if is_text_file(file_path):
            return f"{file_name} is a TXT file"
        else:
            return f"{file_name}: File type not recognized"

    # 매직 넘버로 파일 검사 (다른 형식들)
    detected_type = check_magic_number(file_path)
    
    if detected_type:
        return f"{file_name} is a {detected_type}"
    
    return f"{file_name}: File type not recognized"

# 디렉토리 내 모든 파일 검사
def check_directory_files(directory_path):
    results = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        
        if os.path.isfile(file_path):
            result = check_file(file_path)
            results.append(result)

    return results

# 결과 출력
results = check_directory_files(DIR_PATH)
for result in results:
    print(result)
