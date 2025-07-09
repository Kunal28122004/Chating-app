from fastapi import FastAPI
import socketio
from auth import router as auth_router
from server.models import SessionLocal, Message
from datetime import datetime

sio = socketio.AsyncServer(cors_allowed_origins="*")
fastapi_app = FastAPI()
fastapi_app.include_router(auth_router)
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

@sio.event
async def connect(sid, environ):
    print("User connected:", sid)

@sio.event
async def disconnect(sid):
    print("User disconnected:", sid)

@sio.event
async def send_message(sid, data):
    print("Message received:", data)
    db = SessionLocal()
    message = Message(username=data['username'], content=data['message'], timestamp=datetime.utcnow())
    db.add(message)
    db.commit()
    await sio.emit("receive_message", {"username": data['username'], "message": data['message']})