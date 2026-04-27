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
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: sans-serif;
        }

        #video {
            max-width: 100vw;
            max-height: 100vh;
            object-fit: contain;
        }

        #title {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-size: 16px;
        }

        #btn {
            position: absolute;
            bottom: 20px;
            right: 20px;
            padding: 10px 15px;
            background: white;
            border: none;
            cursor: pointer;
            border-radius: 8px;
        }
    </style>
</head>

<body>

<div id="title">📷 Ompok Feeder Live</div>

<img id="video">

<button id="btn" onclick="toggleFullScreen()">⛶ Fullscreen</button>

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<script>
const socket = io();
const img = document.getElementById("video");

socket.on("frame", (data) => {
    requestAnimationFrame(() => {
        img.src = "data:image/jpeg;base64," + data;
    });
});

function isMobile() {
    return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// 🔥 Fullscreen + Auto rotate
function toggleFullScreen() {
    const elem = document.documentElement;

    if (!document.fullscreenElement) {
        elem.requestFullscreen().then(() => {

            // 📱 ถ้าเป็นมือถือ → บังคับ landscape
            if (isMobile() && screen.orientation) {
                screen.orientation.lock("landscape").catch(() => {});
            }

        });
    } else {
        document.exitFullscreen();

        // 🔄 ปลดล็อก orientation
        if (screen.orientation) {
            screen.orientation.unlock();
        }
    }
}
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@socketio.on('frame')
def handle_frame(data):
    socketio.emit('frame', data)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=10000,
        debug=False
    )