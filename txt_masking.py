import os, re
from datetime import datetime

def mask_content(content):
    jumin_mask = r'([0-9]{6})\s*[-–—]?\s*([1-4])([0-9]{6})'
    phone_mask = r'(\d{2,3})\s*[-–—]\s*(\d{3,4})\s*[-–—]\s*(\d{4})'
    email_mask = r'[:\s]*([a-zA-Z0-9._%+-]{2})([a-zA-Z0-9._%+-]*)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    no_find = 0
    # 주민등록번호 마스킹 (뒷자리 첫 번째 숫자는 표시)
    if re.search(jumin_mask, content):
        content = re.sub(jumin_mask, r'\1- \2******', content)
        no_find = 1
    # 전화번호 마스킹 (중간 4자리 마스킹)
    if re.search(phone_mask, content):
        content = re.sub(phone_mask, r'\1-****-\3', content)
        no_find = 1
    # 이메일 마스킹 (이름 부분에서 앞 두 글자만 남기고 마스킹)
    if re.search(email_mask, content):
        content = re.sub(email_mask, r'\1****@\3', content)
        no_find = 1
    if no_find == 0:
        print('중요정보 포함되어 있지 않음')
    return content


# 파일 경로 및 읽기
DIR_PATH = ''
file_name = 'test.txt'
file_path = os.path.join(DIR_PATH, file_name)
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 파일 내용 마스킹 처리
content = mask_content(content)

now = datetime.now()
day = now.strftime("%Y-%m-%d")

#파일 날짜별 저장
new_file = f'{day}_{file_name}(수정)'
with open(new_file, 'w', encoding='utf-8') as file:
    file.write(content)
