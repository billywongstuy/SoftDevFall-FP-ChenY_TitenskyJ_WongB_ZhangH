from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, hashlib, os

app = Flask(__name__)


@app.route("/")
def login():
    if 'username' in session:
        return redirect("/home")
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")



if __name__ == "__main__":
    app.debug = True
    app.run()
