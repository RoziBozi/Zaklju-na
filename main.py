from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")
@app.route("/")
def main():
    return render_template("charts.html")
@app.route("/")
def main():
    return render_template("choice.html")
@app.route("/")
def main():
    return render_template("first_page.html")
@app.route("/")
def main():
    return render_template("login.html")
@app.route("/")
def main():
    return render_template("news.html")
@app.route("/")
def main():
    return render_template("register.html")

app.run(debug = True)