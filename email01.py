import smtplib, mimetypes, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from dotenv import load_dotenv

# .env 파일 로드하여 환경 변수 설정
load_dotenv()

# 발신자 이메일 및 비밀번호 가져오기
send_email = os.getenv("SECRET_ID")  # 환경 변수에서 발신자 이메일 로드
send_pwd = os.getenv("SECRET_PASS")  # 환경 변수에서 발신자 비밀번호 로드
recv_email = os.getenv("RECEIVER_EMAIL")

# SMTP 서버 설정
smtp_name = "smtp.naver.com"  # 네이버 SMTP 서버 주소
smtp_port = 587  # SMTP 포트 번호

# 첨부파일이 포함된 이메일을 보내는 함수 정의
def main(subject, body, to_email, file_path):
    # 이메일 메시지 객체 생성
    msg = MIMEMultipart()
    msg['Subject'] = subject  
    msg['From'] = send_email  
    msg['To'] = to_email  
    
    # 이메일 본문 추가 (UTF-8 인코딩)
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 첨부파일이 존재하는 경우 처리
    if file_path:
        with open(file_path, 'rb') as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            msg.attach(attachment)
    
    # 이메일 전송 시도
    try:
        smtp = smtplib.SMTP(smtp_name, smtp_port)  
        smtp.ehlo()
        smtp.starttls() 
        smtp.login(send_email, send_pwd)  
        smtp.sendmail(send_email, to_email, msg.as_string()) 
        smtp.quit() 
        print("이메일 전송 완료!") 
    except Exception as e:
        print("이메일 전송 실패:", e) 

if __name__ == '__main__':
    subject = "마스킹 처리된 파일입니다."
    body = "이메일 본문 내용입니다."
    to_email = recv_email  # 환경 변수에서 수신자 이메일 가져오기
    file_path = None  # 첨부파일이 필요하면 파일 경로를 입력하세요

    main(subject, body, to_email, file_path)