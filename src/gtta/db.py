import sqlite3
from datetime import datetime
import os

DB_PATH = "fleet_inbox.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                status TEXT,
                result TEXT,
                created_at TEXT
            )
        """)

def add_job(topic: str) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO jobs (topic, status, result, created_at) VALUES (?, ?, ?, ?)",
                    (topic, "PENDING", "", datetime.now().isoformat()))
        return cur.lastrowid

def update_job(job_id: int, status: str, result: str = ""):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE jobs SET status = ?, result = ? WHERE id = ?", (status, result, job_id))

def get_inbox():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute("SELECT * FROM jobs ORDER BY id DESC")]
