import sqlite3
from datetime import datetime
from config import DATABASE_NAME


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
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
    conn.close()


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def save_subscription(user_id, username, subscription, payment_id, expires_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users
    (user_id, username, subscription, payment_id, expires_at, status)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        username=excluded.username,
        subscription=excluded.subscription,
        payment_id=excluded.payment_id,
        expires_at=excluded.expires_at,
        status='active'
    """, (
        user_id,
        username,
        subscription,
        payment_id,
        expires_at,
        "active"
    ))

    conn.commit()
    conn.close()


def has_active_subscription(user_id):
    user = get_user(user_id)

    if not user:
        return False

    if user["status"] != "active":
        return False

    try:
        return datetime.fromisoformat(user["expires_at"]) > datetime.utcnow()
    except:
        return False


def deactivate_expired():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET status='expired'
    WHERE expires_at IS NOT NULL
      AND expires_at < ?
    """, (datetime.utcnow().isoformat(),))

    conn.commit()
    conn.close()
