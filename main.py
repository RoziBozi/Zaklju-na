from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import yfinance as yf
import pandas as pd

app = Flask(__name__)

conn = sqlite3.connect("main.db")

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, gmail TEXT, password TEXT)")

conn.commit()
conn.close()

@app.route("/")
def main():
    return render_template("first_page.html")


@app.route("/index", methods = ["POST","GET"])
def index():
    if request.method == "POST":
        choice = request.form["choice"]

        choice = yf.Ticker(choice.upper())
        data = choice.history(period="1d")
        
        if data.empty:
            return jsonify({"error": "No data found"})



        price_open = round(data["Open"].values[0],2)
        price_close = round(data["Close"].values[0],2)
        low_price = round(data["Low"].values[0],2)
        high_price = round(data["High"].values[0],2)
        volume = int(data["Volume"].values[0])
        
        stock = {"price_open": price_open, "price_close": price_close, "low_price": low_price, "high_price": high_price, "volume": volume}
        
        
        print(stock)
        return jsonify(stock)


        
    


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
        print(username_gmail, password)

        with sqlite3.connect("main.db") as conn:
            c = conn.cursor()
            
            uporabniki = c.execute("SELECT username, gmail, password FROM users")
            uporabniki = c.fetchall()
            for user in uporabniki:

                if user[0] == username_gmail or user[1] == username_gmail:
                    if user[2] == password:
                        print("login successful")
                        return "login successful"
                    else:
                        return "password is incorrect"
                
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
        print(username, password, gmail)
        with sqlite3.connect("main.db") as conn:
            c = conn.cursor()

            uporabniki = c.execute("SELECT username, gmail FROM users")
            print(uporabniki)
            for user in uporabniki:
                print(user)
                if user[0] == username:
                    c.close()
                    return "Username already taken"
                elif user[1] == gmail:
                    c.close()
                    return "Gmail already taken"

            c.execute("INSERT INTO users (username, gmail, password) VALUES (?, ?, ?)", (username, gmail, password))  

            conn.commit()
        return "Registration successful"

    return render_template("register.html")

app.run(debug = True)