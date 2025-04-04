from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("main.db")

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, gmail TEXT, password TEXT)")

c.execute("SELECT * from users")

conn.commit()
conn.close()

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


@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password =  request.form["password"]
    
        print(username, password)
    return render_template("login.html")


@app.route("/news")
def news():
    return render_template("news.html")


@app.route("/register", methods = ["POST","GET"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password =  request.form["password"]
        gmail = request.form["gmail"]
    
        data = [(username,gmail,password)]
        conn = sqlite3.connect("main.db")
        c = conn.cursor()
        
        c.execute("SELECT username, gmail FROM users WHERE username = ? OR gmail = ?", (username, gmail))

        for user in c:
            if username == user[0]:
                
                return "Username already taken" 
            elif gmail == user[1]:
                
                return "Gmail already taken"

        c.execute("INSERT INTO users (username, gmail, password) VALUES (?, ?, ?)", (username, gmail, password))  

        conn.commit()
        conn.close()

    return render_template("register.html")

app.run(debug = True)