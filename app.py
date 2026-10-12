from flask import Flask, render_template, request, redirect
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

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL,
            password TEXT NOT NULL
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

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/do_register", methods=["POST"])
def do_register():
    account=request.form.get("account")
    password=request.form.get("password")
    conn=get_db()
    conn.execute("INSERT INTO accounts (account,password) VALUES (?,?)",(account,password))
    conn.commit()
    conn.close()
    return "注册成功,快去/login登录!"
@app.route("/login")
def login():
    msg=request.args.get("msg")
    return render_template("login.html",msg=msg)

@app.route("/do_login",methods=["POST"])
def do_login():
    account=request.form.get("account")
    password=request.form.get("password")

    conn=get_db()
    row=conn.execute("SELECT * FROM accounts WHERE account=?",(account,)).fetchone()
    print(row)        # 看看 row 长什么样
    print(type(row))  # 看看它的类型
    conn.close()
    if row is None:
        return redirect("/login?msg=账号不存在")
    if row["password"]!=password:
        return redirect("/login?msg=密码错误")
    return redirect("/login?msg=登陆成功")


if __name__ == "__main__":
    init_db()      # 启动服务前先建表
    app.run(debug=True)