from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import yfinance as yf
import pandas as pd
import plotly.graph_objects as pl
import time
import requests
import feedparser

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
        data = choice.history(period="1d", interval="1m")

        splosna_data = choice.info
        print(data)
        if data.empty:
            print("No data found")
            return jsonify({"error": "No data found"})

    
        price_open = round(data["Open"].values[0],2)
        price_close = round(data["Close"].values[0],2)
        low_price = round(data["Low"].values[0],2)
        high_price = round(data["High"].values[0],2)
        volume = int(data["Volume"].values[0])
        stock = {"price_open": price_open,
                "price_close": price_close,
                "low_price": low_price,
                "high_price": high_price,
                "volume": volume,
                "name": splosna_data["longName"]
            }
        print(stock)
        return jsonify(stock)


        
    


    return render_template("index.html")

@app.route("/charts", methods = ["POST","GET"])
def charts():
    if request.method == "POST":
        choice = request.form["choice"]
        print(choice)
        choice = yf.Ticker(choice.upper())


        data = choice.history(period="1y")
        
        data.to_csv("data.csv")
        data = pd.read_csv("data.csv")

        chart_data = pl.Candlestick(x=data["Date"],
                            open=data["Open"],
                            high=data["High"],
                            low=data["Low"],
                            close=data["Close"],
                            name=choice.info["longName"],
                            )
        chart = pl.Figure(data=[chart_data])
        chart_za_stran = chart.to_html(full_html=False, include_plotlyjs="cdn")

        return jsonify({"chart": chart_za_stran})

    return render_template("charts.html")

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


@app.route("/news", methods = ["POST","GET"])
def news():
    if request.method == "POST":
        choice = request.form["choice"]
        print(choice)

        news_url_list = ["https://finance.yahoo.com/news/rssindex","https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069","https://feeds.a.dj.com/rss/RSSMarketsMain.xml","https://news.ycombinator.com/rss"]
        
                
        list_artiklov = []

        for news_url in news_url_list:
            artikel = feedparser.parse(news_url)

            for specificen_artikel in artikel.entries:

                if choice.lower() in specificen_artikel.title.lower():
                    list_artiklov.append({
                        "title": specificen_artikel.title,
                        "link": specificen_artikel.link,
                        "published": specificen_artikel.published
                    })
        print(list_artiklov)
        if list_artiklov:
            return jsonify({"article": list_artiklov})
        else:
            return jsonify({"article": {}})

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