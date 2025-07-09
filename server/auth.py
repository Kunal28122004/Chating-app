from fastapi import APIRouter, HTTPException, Form
from server.models import SessionLocal, User
import bcrypt

router = APIRouter()

def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()

@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    if get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(username=username, password=hashed.decode())
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = get_user_by_username(db, username)
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
