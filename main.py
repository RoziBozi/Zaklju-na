from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("main.db")

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, gmail TEXT, password TEXT)")

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
        username_gmail = request.form["username"]
        password =  request.form["password"]
    
        with sqlite3.connect("main.db") as conn:
            c = conn.cursor()

            uporabniki = c.execute("SELECT username, gmail, password FROM users")

            for user in uporabniki:
                print(user)
                if user[0] == username_gmail:
                    if user[2] == password:
                        c.close()
                        return redirect(url_for("index"))
                    else:
                        c.close()
                        return "password is incorrect"
                elif user[1] == username_gmail:
                    if user[2] == password:
                        c.close()
                        return redirect(url_for("index"))
                    else:
                        c.close()
                        return "password is incorrect"
                else:
                    c.close()
                    return "username or gmail is incorrect"
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
    
        with sqlite3.connect("main.db") as conn:
            c = conn.cursor()

            uporabniki = c.execute("SELECT username, gmail FROM users")

            for user in uporabniki:
                print(user)
                if user[0] == username:
                    c.close()
                    return "Username already taken"
                elif user[1] == gmail:
                    c.close()
                    return "Gmail already taken"

            c.execute("INSERT INTO users (username, gmail, password) VALUES (?, ?, ?)", (password, gmail, username))  

            conn.commit()
        return "Registration successful"

    return render_template("register.html")

app.run(debug = True)