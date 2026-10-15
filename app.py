from flask import Flask, render_template, request, redirect,session
import sqlite3
from werkzeug.utils import secure_filename 
import os

# static uploads的绝对路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads")
# 数据库文件的绝对路径（和 app.py 同目录，不管谁运行都指向同一个文件）
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market.db")

app = Flask(__name__)

app.secret_key="campus-market-2026"
# 连接数据库（文件不存在会自动创建）
def get_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT
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
    conn.close()
    if row is None:
        return redirect("/login?msg=账号不存在")
    if row["password"]!=password:
        return redirect("/login?msg=密码错误")
    session["account"]=account
    return redirect("/")

@app.route("/publish")
def publish():
    msg=request.args.get("msg")
    return render_template("publish.html",msg=msg)

@app.route("/do_publish",methods=["POST"])
# 发布商品,将商品信息载入数据库
def do_publish():
    if "account" not in session:
        return redirect("/login?msg=请先完成登录")
    title=request.form.get("title")
    price=float(request.form.get("price"))
    description=request.form.get("description")
    # 加图片
    image_file=request.files.get("image")
    image_name=""
    if image_file and image_file.filename!="":
        image_name=secure_filename(image_file.filename)
        image_file.save(os.path.join(UPLOAD_FOLDER,image_name))
    conn=get_db()
    conn.execute("INSERT INTO items (title,price,description,image) VALUES (?,?,?,?)",
                 (title,price,description,image_name)
                 )
    conn.commit()
    conn.close()
    return redirect("/publish?msg=发布成功")

@app.route("/items")
# 陈列物品的编号,标题和价格,以及跳转到详情页
def items():
    q = request.args.get("q")          # 取搜索词，没搜时是 None
    conn = get_db()
    if q:
        rows = conn.execute(
            "SELECT * FROM items WHERE title LIKE ?", (f"%{q}%",)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    result="相关书籍:<br>"
    
    for row in rows:
        result+=f"编号:{row['id']} 标题:{row['title']} 价格:{row['price']} <a href='/item/{row['id']}'>查看详情</a><br>"
    return result

@app.route("/item/<int:item_id>")
def item_detail(item_id):
    conn=get_db()
    row=conn.execute("SELECT * FROM items WHERE id=?",(item_id,)).fetchone()
    conn.close()
    if row is None:
        return "商品不存在"
    else:
        img_html=f'<img src="/static/uploads/{row['image']}" width="300">' if row['image'] else ""
        return f"标题:{row['title']}<br>价格:{row['price']}<br>描述:{row['description']}<br>{img_html}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

init_db()      # 启动服务前先建表

if __name__ == "__main__":

    app.run()