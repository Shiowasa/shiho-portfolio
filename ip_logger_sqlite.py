
import requests
from datetime import datetime
import time
import sqlite3
import os

DB_DIR = "ip_logs"        # ログ保存ディレクトリ
INTERVAL = 60             # 取得間隔（秒）

def get_global_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception as e:
        return f"Error: {e}"

def get_db_path():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    return os.path.join(DB_DIR, f"{today}.db")

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ip_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ip TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_ip():
    ip = get_global_ip()
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_path = get_db_path()
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO ip_log (timestamp, ip) VALUES (?, ?)", (time_str, ip))
    conn.commit()
    conn.close()

    print(f"[{time_str}] IP: {ip} -> {db_path}")

if __name__ == "__main__":
    print("=== IP Logger with SQLite Started ===")
    while True:
        log_ip()
        time.sleep(INTERVAL)


