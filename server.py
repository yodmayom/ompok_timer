import asyncio
import websockets
from flask import Flask
import threading
import os

clients = set()
#websocket server
async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

#flask app
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>กล้องจากบ่อให้อาหารปลาชะโอนที่เรือนเกษตร</h1>

    <script>
        const ws = new WebSocket('ws://localhost:8765');
        
        ws.binaryType = "blob";

        ws.onmessage = function(event) {
            const url = URL.createObjectURL(event.data);
            document.getElementById('video').src = url;
        };
    </script>
    """

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ws_server = websockets.serve(handler, "0.0.0.0", 8765)
    loop.run_until_complete(ws_server)
    loop.run_forever()
if __name__ == '__main__':
    t = threading.Thread(target = start_websocket_server)
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)