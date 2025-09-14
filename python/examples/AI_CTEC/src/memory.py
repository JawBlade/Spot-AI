import sqlite3
from datetime import datetime

DB_PATH = "./data/spot_memory.db"

def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_message TEXT NOT NULL,
            spot_response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_conversation(user_msg, spot_response, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversation_history (user_message, spot_response)
        VALUES (?, ?)
    """, (user_msg, spot_response))
    conn.commit()
    conn.close()

def get_last_conversations(limit=5, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_message, spot_response
        FROM conversation_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]  # oldest first

def clear_history(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversation_history")
    conn.commit()
    conn.close()
