import re
import zipfile
from lxml import etree

def mask_content(content):
    masked = False  # 마스킹 여부 추적

    # 주민등록번호 마스킹 (숫자가 붙어있을 때도 처리)
    jumin_pattern = r'([0-9]{6})\s*[-–—]?\s*([1-4])([0-9]{6})'
    if re.search(jumin_pattern, content):
        content = re.sub(jumin_pattern, r'\1-\2******', content)
        masked = True
    
    # 전화번호 마스킹
    phone_pattern = r'(\d{2,3})\s*[-–—]\s*(\d{3,4})\s*[-–—]\s*(\d{4})'
    if re.search(phone_pattern, content):
        content = re.sub(phone_pattern, r'\1-****-\3', content)
        masked = True
    
    # 이메일 마스킹
    email_pattern = r'[:\s]*([a-zA-Z0-9._%+-]{2})([a-zA-Z0-9._%+-]*)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    if re.search(email_pattern, content):
        content = re.sub(email_pattern, r'\1****@\3', content)
        masked = True

    return content, masked


def process_document(input_file):
    # 마스킹된 파일 저장 경로
    new_file_path = input_file.replace('.docx', '_마스킹.docx')
    masked_flag = False  # 전체 문서에서 마스킹 여부 추적

    # DOCX 파일을 ZIP 파일로 읽기
    with zipfile.ZipFile(input_file, 'r') as zin:
        # 새로운 ZIP 파일 생성
        with zipfile.ZipFile(new_file_path, 'w') as zout:
            # DOCX 파일의 모든 파일 순회
            for item in zin.infolist():
                # 파일 내용 읽기
                buffer = zin.read(item.filename)
                # "word/document.xml" 파일인 경우 텍스트 내용 마스킹
                if item.filename == 'word/document.xml':
                    # XML 파싱
                    root = etree.fromstring(buffer)
                    # 모든 텍스트 요소 순회하며 마스킹 적용
                    for text_element in root.xpath('//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                        text = text_element.text
                        if text:
                            masked_text, masked = mask_content(text)  # mask_content 함수 사용
                            text_element.text = masked_text
                            if masked:
                                masked_flag = True  # 마스킹이 한 번이라도 되면 플래그 설정
                    # 수정된 XML 내용을 문자열로 변환
                    buffer = etree.tostring(root)
                # 파일 압축
                zout.writestr(item, buffer)

    return new_file_path, masked_flag

# 출력을 위한 실행 구문
if __name__ == "__main__":
    input_file = '2025년_신입사원(최신화).docx'  # 처리할 DOCX 파일의 경로
    masked_file_path, masked_flag = process_document(input_file)
    
    if masked_flag:
        print(f"마스킹된 파일 저장 위치: {masked_file_path}")
    else:
        print("중요 정보가 포함되어 있지 않음")
