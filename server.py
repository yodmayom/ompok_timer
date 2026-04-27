from flask import Flask, render_template_string
from flask_socketio import SocketIO
import os

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
    <title>Ompok</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            margin: 0;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: sans-serif;
        }

        /* 📦 กล่องวิดีโอ */
        .box {
            width: 85vw;
            height: 85vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        /* 🎯 ปุ่มคอม */
        #pcBtn {
            position: absolute;
            bottom: 15px;
            right: 15px;
            padding: 10px 14px;
            border: none;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            font-size: 14px;
        }

        /* 📱 ปุ่มมือถือ */
        #mobileBtn {
            display: none;
            position: absolute;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            padding: 16px 28px;
            font-size: 18px;
            border: none;
            border-radius: 12px;
            background: #00ff88;
            font-weight: bold;
        }

        /* 📱 mobile */
        @media (max-width: 768px) {
            .box {
                width: 100vw;
                height: 100vh;
            }

            #mobileBtn {
                display: block;
            }

            #pcBtn {
                display: none;
            }
        }
    </style>
</head>

<body>

<div class="box">
    <img id="video">
</div>

<button id="pcBtn" onclick="togglePC()">Fullscreen</button>
<button id="mobileBtn" onclick="toggleMobile()">ดูเต็มจอ</button>

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<script>
const socket = io();
const img = document.getElementById("video");

socket.on("frame", (data) => {
    requestAnimationFrame(() => {
        img.src = "data:image/jpeg;base64," + data;
    });
});

/* 💻 PC fullscreen */
function togglePC() {
    const elem = document.documentElement;

    if (!document.fullscreenElement) {
        elem.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

/* 📱 Mobile fullscreen + landscape */
function toggleMobile() {
    const elem = document.documentElement;

    elem.requestFullscreen().then(() => {
        if (screen.orientation) {
            screen.orientation.lock("landscape").catch(() => {});
        }
    });
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
    port = int(os.environ.get("PORT", 10000))

    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False
    )