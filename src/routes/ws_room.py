from enum import Enum
from typing import TypedDict

import socketio
from src.libs import sio


class QuizEvents(str, Enum):
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    SUBMIT_ANSWER = "submit_answer"


class QuizRoomNameSpace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        await self.emit("message", f"User {sid} connected to quiz space")
    
    async def on_disconnect(self, sid):
        await self.emit("message", f"User {sid} disconnected from quiz space")
    
    async def on_submit_answer(self, sid, data):
        session_data = await self.get_session(sid)
        room = session_data.get("room")
        await self.emit(QuizEvents.SUBMIT_ANSWER, data, room=room)
    
    async def on_join_room(self, sid, data, *args, **kwargs):
        room = data.get('room')
        self.enter_room(sid, room)
        message = {"message": f"User {sid} joined room {room}"}
        await self.save_session(sid, {"room": room})
        await self.emit(QuizEvents.JOIN_ROOM, message, room=room)

    async def on_leave_room(self, sid, data):
        session_data = await self.get_session(sid)
        room = session_data.get("room")
        message = {"message": f"User {sid} left room {room}"}
        self.leave_room(sid, room)
        await self.emit(QuizEvents.LEAVE_ROOM, message, room=room)