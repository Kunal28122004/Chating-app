### 💾 Message Storage
All chat messages are stored in `chat.db` (SQLite) with:
- `username`
- `content`
- `timestamp`

You can inspect the database using `server/view_db.py`.

```bash
python server/view_db.py
