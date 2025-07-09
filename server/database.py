# main.py

from fastapi import FastAPI, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, SessionLocal
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# FastAPI app
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode("utf-8"))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully."}

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"message": "Login successful"}

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Received message from {sid}: {data}")
    await sio.emit("message", data)

# Run app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(sio_app, port=8000)
