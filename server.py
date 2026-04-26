from flask import Flask, request, send_file
import os

app = Flask(__name__)

UPLOAD_PATH = '/tmp/latest.jpg'

@app.route('/')
def home():
    return """
    <h1>กล้องจากบ่อปลาชะโอนที่เรือนเกษตร (ชั่วคราว)</h1>
    <img src="/view" width="400>
    <meta http-equiv="refresh" content="1">
    """

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['frame']
    file.save(UPLOAD_PATH)
    return 'OK'

@app.route('/view')
def view():
    if os.path.exists(UPLOAD_PATH):
        return send_file(UPLOAD_PATH, mimetype='image/jpeg')
    return 'No image available'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)