from flask import Flask, request, send_file
import os

app = Flask(__name__)

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
    file.save('latest.jpg')
    return 'OK'

@app.route('/view')
def view():
    if os.path.exists('latest.jps'):
        return send_file('latest.jpg', mimetype='image/jpeg')
    return 'Np image available'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)