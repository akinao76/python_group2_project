import ftplib

#FTP 파일 다운로드
def download_file(ftp, filename):
    with open('./'+filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

#FTP 로그인
ftp = ftplib.FTP("192.168.86.128")
ftp.login('msfadmin','msfadmin')
#FTP 파일 경로 입력
DIR_PATH = input('DIR PATH : ')
filename = input('File name : ')
#FTP 서버 파일 위치 이동
ftp.cwd(DIR_PATH)

download_file(ftp, filename)

ftp.quit()
