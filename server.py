from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

HTML = """
<h2>📷 Live Fish Camera</h2>
<img id="video" width="640">

<script src="https://cdn.socket.io/4.0.1/socket.io.min.js"></script>
<script>
const socket = io();

socket.on('frame', function(data) {
    document.getElementById("video").src =
    "data:image/jpeg;base64," + data;
});
</script>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@socketio.on('frame')
def handle_frame(data):
    emit('frame', data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)