from flask import Flask, render_template, request, redirect, url_for, flash, session
import ftplib
import os
import ipaddress
from check_file import *  # 업로드할 파일의 확장자 검사
from masking import *  # 파일 마스킹

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션을 위한 비밀키 설정

UPLOAD_FOLDER = 'uploads'  # 로컬 업로드 폴더
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.xlsx'}  # 허용된 확장자

# 🔹 확장자 검사 함수
def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# 🔹 FTP 파일 업로드 함수
def upload_to_ftp(file_path, filename, ip, usern, password):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login(user=usern, passwd=password)

        project_name = filename.split('_')[0]  # 프로젝트 폴더 분류
        if project_name not in ftp.nlst():
            ftp.mkd(project_name)
        
        ftp.cwd(project_name)  # 폴더 이동 후 저장
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)

        ftp.quit()
        return True
    except Exception as e:
        print(f"FTP 업로드 오류: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ip = request.form.get('ip_address')
        username = request.form.get('username')
        password = request.form.get('password')

        # IP 주소 유효성 검사
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            flash("유효하지 않은 IP 주소입니다.", "danger")
            return redirect(url_for('login'))

        try:
            # FTP 로그인 시도
            ftp = ftplib.FTP(ip)
            ftp.login(user=username, passwd=password)
            ftp.quit()  # 로그인 성공 후 종료

            # 세션에 로그인 정보 저장
            session['ftp_ip'] = ip
            session['ftp_user'] = username
            session['ftp_pass'] = password

            flash("FTP 로그인 성공!", "success")
            return redirect(url_for('upload_page'))  # 업로드 페이지로 이동
        except ftplib.all_errors as e:
            flash(f"FTP 로그인 실패: {e}", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if 'ftp_ip' not in session:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('파일이 선택되지 않았습니다.')
            return redirect(url_for('upload_page'))

        file = request.files['file']
        if file.filename == '':
            flash('파일이 선택되지 않았습니다.')
            return redirect(url_for('upload_page'))

        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # 🔹 파일 검사 수행
        file_type = check_file(file_path)

        # 위험 파일 차단
        if "EXE 파일 차단됨!" in file_type or "바이너리 파일로 의심됨!" in file_type or "파일 형식 확인 불가!" in file_type:
            flash(f"업로드 차단됨: {file_type}")
            os.remove(file_path)  # 위험 파일 즉시 삭제
            return redirect(url_for('upload_page'))

        flash(f"파일 유형 확인됨: {file_type}")

        # 🔹 마스킹 처리
        mask_result = mask_file(file_path)
        flash(mask_result)

        # 🔹 FTP 업로드
        ip, usern, password = session.get('ftp_ip'), session.get('ftp_user'), session.get('ftp_pass')
        if not ip or not usern or not password:
            flash('FTP 로그인 정보가 없습니다. 다시 로그인하세요.')
            return redirect(url_for('login'))

        if upload_to_ftp(file_path, filename, ip, usern, password):
            flash('파일이 성공적으로 업로드되었습니다!')
        else:
            flash('파일 업로드에 실패했습니다.')

        os.remove(file_path)  # 로컬 파일 삭제
        return redirect(url_for('upload_page'))

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
