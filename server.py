from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ompok Camera</title>
    <style>
        body {
            margin: 0;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        #video {
            width: 100vw;   /* 🔥 เต็มจอ */
            height: auto;
        }
    </style>
</head>
<body>

<h2 style="position:absolute; top:10px; color:white;">
📷 Ompok Feeder Live
</h2>

<img id="video">

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script>
const socket = io();

socket.on("frame", (data) => {
    document.getElementById("video").src =
        "data:image/jpeg;base64," + data;
});
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

# 🔥 รับ frame จาก Raspberry Pi
@socketio.on('frame')
def handle_frame(data):
    socketio.emit('frame', data)  # broadcast ทุก client

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=10000,
        debug=False
    )