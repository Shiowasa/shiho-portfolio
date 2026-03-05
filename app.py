from flask import Flask, request,  render_template
import sqlite3
import datetime
import os

app = Flask(__name__)

# DBフォルダ作成
if not os.path.exists("ip_logs"):
    os.makedirs("ip_logs")

@app.route("/")
def log_ip():
    ip = request.remote_addr
    today = datetime.date.today().strftime("%Y-%m-%d")
    db_path = f"ip_logs/{today}.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            timestamp TEXT
        )
    """)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO logs (ip, timestamp) VALUES (?, ?)", (ip, now))

    conn.commit()
    conn.close()

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)