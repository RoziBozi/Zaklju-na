from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("first_page.html")
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/charts")
def charts():
    return render_template("charts.html")
@app.route("/choice")
def choice():
    return render_template("choice.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/news")
def news():
    return render_template("news.html")
@app.route("/register")
def register():
    return render_template("register.html")

app.run(debug = True)