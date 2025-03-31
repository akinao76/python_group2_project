import os

# 파일 확장자 (매직 넘버)
MAGIC_NUMBERS = {
    b'\x25\x50\x44\x46': 'PDF file',  # %PDF
    b'\x50\x4B\x03\x04': 'DOCX/XLSX file',  # ZIP 기반 (DOCX, XLSX)
    b'\xFF\xD8\xFF': 'JPEG image file',  # JPG
    b'\x89\x50\x4E\x47': 'PNG image file',  # PNG
    b'\x4D\x5A': 'EXE file',  # EXE (MZ)
}

# 매직 넘버 검사 함수
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

# 파일 검사 함수 (EXE 위장 탐지 포함)
def check_file(file_path):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1].lower()

    # 매직 넘버 검사
    detected_type = check_magic_number(file_path)

    # EXE 파일 차단 (위장 방지)
    if detected_type == 'EXE file':
        return f"{file_name}: EXE 파일 차단됨!"

    # TXT 파일이라면 추가 검사 수행
    if file_extension == '.txt':
        # UTF-8로 읽을 수 있는지 확인
        if is_text_file(file_path):
            return f"{file_name} is a TXT file"
        else:
            return f"{file_name}: 바이너리 파일로 의심됨!"

    # 다른 파일 유형 검사
    if detected_type:
        return f"{file_name} is a {detected_type}"
    
    return f"{file_name}: 파일 형식 확인 불가!"
