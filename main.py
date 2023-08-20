import socketio
from fastapi import FastAPI

from src.libs import sio
from src.routes import QuizRoomNameSpace

app = FastAPI()

sio.register_namespace(QuizRoomNameSpace("/quiz"))
sio_asgi_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)

app.add_route("/socket.io/", route=sio_asgi_app, methods=["GET", "POST"])
app.add_websocket_route("/socket.io/", sio_asgi_app)


@app.get("/")
async def root():
    await sio.emit("message", "hello everyone")
    return {
        "message": "Quiz Websocket Proof of Concept",
        "routes": {
            "docs": "/docs",
        }
    }