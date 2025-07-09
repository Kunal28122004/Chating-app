from models import SessionLocal, User, Message  # <- assuming you renamed db.py to database.py

db = SessionLocal()

print("📋 Users:")
for user in db.query(User).all():
    print(f"ID: {user.id}, Username: {user.username}")

print("\n💬 Messages:")
for msg in db.query(Message).all():
    print(f"{msg.timestamp} - {msg.username}: {msg.content}")
