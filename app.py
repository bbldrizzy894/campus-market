from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! 我的项目跑起来了"

if __name__ == "__main__":
    app.run(debug=True)