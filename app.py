from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)
app.debug = True

@app.route("/hello/<name>")
def hello_name(name):
    return f"hello {escape(name)}"

@app.route("/hello/")
def hello():
    name = request.args.get("x")
    return f"hello {escape(name)}"

@app.route("/")
def index():
    return render_template("test_1.html")
