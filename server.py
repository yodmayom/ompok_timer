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
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
            font-family: sans-serif;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        .box {
            width: 75vw;
            height: 75vh;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 12px;
            overflow: hidden;
        }

        img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        #pcBtn {
            padding: 10px 16px;
            border: none;
            border-radius: 10px;
            background: white;
            cursor: pointer;
        }

        #mobileBtn {
            display: none;
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            padding: 16px 28px;
            font-size: 18px;
            border: none;
            border-radius: 12px;
            background: #00ff88;
            font-weight: bold;
        }

        @media (max-width: 768px) {
            .box {
                width: 100vw;
                height: 100vh;
                border-radius: 0;
            }

            #pcBtn {
                display: none;
            }

            #mobileBtn {
                display: block;
            }
        }
    </style>
</head>

<body>

<div class="container">
    <div class="box">
        <img id="video">
    </div>

    <!-- 💻 PC -->
    <button id="pcBtn" onclick="togglePC()">Zoom Video</button>
</div>

<!-- 📱 Mobile -->
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

/* 💻 PC: zoom เฉพาะ video */
function togglePC() {
    if (!document.fullscreenElement) {
        img.requestFullscreen().catch(err => console.log(err));
    } else {
        document.exitFullscreen();
    }
}

/* 📱 Mobile: zoom video + landscape */
function toggleMobile() {
    img.requestFullscreen().then(() => {

        // Android: lock landscape (ถ้ารองรับ)
        if (screen.orientation && screen.orientation.lock) {
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