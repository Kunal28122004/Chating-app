from fastapi import FastAPI
import socketio
from auth import router as auth_router
from server.models import SessionLocal, Message
from datetime import datetime
from fastapi import Query
from typing import List


sio = socketio.AsyncServer(cors_allowed_origins="*")
fastapi_app = FastAPI()
fastapi_app.include_router(auth_router)
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

# Room naming helper
def get_room_name(user1, user2):
    return "__".join(sorted([user1, user2]))

# On client connect
@sio.event
async def connect(sid, environ):
    print(f"User connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"User disconnected: {sid}")

# User joins a private chat room with another user
@sio.event
async def join(sid, data):
    """
    data = {
        'user1': 'alice',
        'user2': 'bob'
    }
    """
    room = get_room_name(data['user1'], data['user2'])
    sio.enter_room(sid, room)
    print(f"{data['user1']} joined room: {room}")

# Send message in a private room
@sio.event
async def send_message(sid, data):
    """
    data = {
        'sender': 'alice',
        'receiver': 'bob',
        'message': 'Hello'
    }
    """
    room = get_room_name(data['sender'], data['receiver'])
    db = SessionLocal()

    message = Message(
        sender=data['sender'],
        receiver=data['receiver'],
        content=data['message'],
        timestamp=datetime.utcnow()
    )
    db.add(message)
    db.commit()

    await sio.emit("receive_message", {
        "sender": data['sender'],
        "message": data['message'],
        "timestamp": message.timestamp.isoformat()
    }, room=room)
@fastapi_app.get("/messages")
def get_messages(user1: str = Query(...), user2: str = Query(...)):
    db = SessionLocal()
    room_users = {user1, user2}
    messages = db.query(Message).filter(
        Message.sender.in_(room_users),
        Message.receiver.in_(room_users)
    ).order_by(Message.timestamp).all()

    return [{
        "sender": m.sender,
        "receiver": m.receiver,
        "message": m.content,
        "timestamp": m.timestamp.isoformat()
    } for m in messages]