import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    subscription TEXT,
    payment_id TEXT,
    expires_at TEXT,
    status TEXT
)
""")

conn.commit()
