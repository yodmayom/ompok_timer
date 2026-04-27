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
            overflow: hidden;
            font-family: sans-serif;
        }

        /* 📦 กล่องวิดีโอ */
        #videoBox {
            width: 80vw;
            height: 80vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #000;
        }

        #video {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        #title {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
        }

        /* 💻 ปุ่มคอม */
        #btnPC {
            position: absolute;
            bottom: 20px;
            right: 20px;
            padding: 10px 15px;
            background: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        /* 📱 ปุ่มมือถือ (ใหญ่) */
        #btnMobile {
            display: none;
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            padding: 18px 30px;
            font-size: 20px;
            background: #00ff88;
            border: none;
            border-radius: 12px;
            font-weight: bold;
        }

        /* 📱 mobile mode */
        @media (max-width: 768px) {
            #videoBox {
                width: 100vw;
                height: 100vh;
            }

            #btnMobile {
                display: block;
            }

            #btnPC {
                display: none;
            }
        }
    </style>
</head>

<body>

<div id="title">📷 Ompok Feeder Live</div>

<div id="videoBox">
    <img id="video">
</div>

<!-- 💻 desktop -->
<button id="btnPC" onclick="openFullPC()">⛶ Fullscreen</button>

<!-- 📱 mobile -->
<button id="btnMobile" onclick="openMobile()">📱 ซูมเต็มจอ</button>

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

/* 💻 คอมเต็มจอ */
function openFullPC() {
    const elem = document.documentElement;

    if (!document.fullscreenElement) {
        elem.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

/* 📱 มือถือ + landscape */
function openMobile() {
    const elem = document.documentElement;

    elem.requestFullscreen().then(() => {

        // บังคับแนวนอน
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
    socketio.run(
        app,
        host="0.0.0.0",
        port=10000,
        debug=False
    )