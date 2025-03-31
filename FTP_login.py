import os, ftplib, ipaddress
from flask import Flask, flash, request,render_template,redirect

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    ip = request.form['ip_address']
    usern = request.form['username']
    password = request.form['password']

    # IP 주소 유효성 검사
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        flash("유효하지 않은 IP 주소입니다.")
        return redirect('index')

    try:
        # FTP 서버에 연결
        ftp = ftplib.FTP(ip)
        ftp.login(user=usern, passwd=password)


        ftp.quit()  # 연결 종료

        return render_template('index.html')  # 다음 페이지로 이동

    except ftplib.error_perm as e:
        flash(f"FTP 권한 오류: {e}")
        return redirect('index')
    except ftplib.error_temp as e:
        flash(f"FTP 일시적인 오류: {e}")
        return redirect('index')
    except ftplib.all_errors as e:
        flash(f"FTP 로그인 실패: {e}. IP 주소, 아이디, 비밀번호를 확인하세요.")
        return redirect('index')

