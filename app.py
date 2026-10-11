from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 连接数据库（文件不存在会自动创建）
def get_db():
    conn = sqlite3.connect("market.db")
    conn.row_factory = sqlite3.Row  # 让查询结果可以像字典一样用
    return conn

# 启动时建表（表已存在则跳过）
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    name = request.args.get("username")
    conn = get_db()
    conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return f"你好，{name}！你的名字已经存入数据库"

@app.route("/users")
def users():
    conn = get_db()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    result = "数据库里已有这些名字：<br>"
    for row in rows:
        result += f"id={row['id']} 名字={row['name']}<br>"
    return result

if __name__ == "__main__":
    init_db()      # 启动服务前先建表
    app.run(debug=True)