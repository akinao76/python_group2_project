from flask import Flask, app, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
   

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(f'uploads/{file.filename}')
        return render_template('index.html', message='File uploaded successfully')
    else:
        return render_template('index.html', error='No file selected')

if __name__ == '__main__':
    app.run(debug=True)
