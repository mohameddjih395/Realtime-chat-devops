from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat en temps réel</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <textarea id="chat" cols="100" rows="20" readonly></textarea><br>
        <input type="text" id="messageInput" autocomplete="off"/>
        <button onclick="sendMessage()">Envoyer</button>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var chat = document.getElementById('chat');
                chat.value += event.data + '\\n';
            };
            function sendMessage() {
                var input = document.getElementById("messageInput");
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message reçu : {data}")
    except WebSocketDisconnect:
        print("Client déconnecté")

