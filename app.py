from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    name = request.args.get("username")
    return f"你好，{name}！欢迎你来到我的网站"

if __name__ == "__main__":
    app.run(debug=True)