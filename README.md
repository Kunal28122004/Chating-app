# 💬 Simple Chat App

### 🎯 Introduction
The **Simple Chat App** is a lightweight chat application designed to demonstrate core messaging functionality. It allows users to send and receive messages in real-time while storing all communication in a **SQLite** database. This project serves as a great starting point for developers looking to build or extend real-time chat solutions.

---

### 🚀 Features
- 🔐 Optional user authentication
- 💬 Real-time message display
- 🗃️ Message storage using **SQLite**
- 🧰 View stored messages via `view_db.py`
- 🔎 Easy message inspection & database management
- 🎨 Modular and customizable components

---

### 🗄️ Database Structure

The **chat.db** SQLite database consists of a single table, **messages**, with the following structure:

| Column Name | Type     | Description                             |
|-------------|----------|-----------------------------------------|
| `id`        | INTEGER  | Primary key, auto-incrementing          |
| `username`  | TEXT     | The name of the user sending the message |
| `content`   | TEXT     | The content of the chat message         |
| `timestamp` | DATETIME | The timestamp when the message was sent |

---

### ⚙️ Setup & Installation

Follow the steps below to run the app locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chat-app.git
2. Navigate to the project directory
   ```bash
  cd chat-app
3. Install the required dependencies
  ```bash
  pip install -r requirements.txt

4. Inspect stored messages
  Use the provided script to view the message database:
  ```bash
  python server/view_db.py
