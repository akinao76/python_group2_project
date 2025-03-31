import os, re

def txt_masking(file_path):
    #개인정보 패턴
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
    jumin_pattern = re.compile(r'\d{6}\s*[-]\s*\d{7}')
    phone_pattern = re.compile(r'(\d{2,3})\s*[-–—]\s*(\d{3,4})\s*[-–—]\s*(\d{4})')

    not_find = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            #주민등록번호 마스킹 처리
            if re.search(jumin_pattern, line):
                jumin = re.search(jumin_pattern, line)[0]
                jumin_mask=jumin.replace(jumin[-6:], '******')
                lines[index]= lines[index].replace(jumin, jumin_mask)
                not_find += 1
            #이메일 마스킹 처리
            if re.search(email_pattern, line):
                email = re.search(email_pattern, line)[0]
                mask = re.search((re.compile(r'[\w\.-]+')), email)[0]
                email_mask = email.replace(mask[2:], '****')
                lines[index] = lines[index].replace(email, email_mask)
                not_find += 1
            #폰번호 마스킹 처리(010-숫자-숫자만 가능)
            if re.search(phone_pattern, line):
                phone = re.search(phone_pattern, line)[0]
                phone_mask = phone.replace(phone[4:8], '****')
                lines[index]= lines[index].replace(phone, phone_mask)
                not_find += 1

    if not_find != 0:
        #마스킹된 파일 생성
        new_file = f'masking_{file_path}'
        with open(new_file, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write(line)
        return new_file
    
    else:
            print("중요정보 포함되어 있지 않음")





#메인 실행
if __name__ == "__main__":
    #파일 경로
    DIR_PATH = ''
    file_name = '주민정보.txt'
    file_path = os.path.join(DIR_PATH, file_name)
    new_file = txt_masking(file_path)
