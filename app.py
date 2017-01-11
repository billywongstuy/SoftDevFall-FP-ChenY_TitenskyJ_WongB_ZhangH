from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, hashlib, os, utils
from utils import auth

app = Flask(__name__)


@app.route("/")
def home():
    if 'username' in session:
        return render_template("home.html")
    return render_template("login.html",message="")


@app.route("/login", methods=['POST'])
def login():
    x=auth.userLogin(request.form['username'],request.form['pw'])
    if x[0]=='True':
        session['username'] = request.form['username']
        return redirect("/")
    if x[0]=='False':
        return render_template("login.html",message=x[1])

@app.route("/register", methods=['POST'])
def register():
    x=auth.addUser(request.form['username'],request.form['pw'],request.form['pwc'],request.form['plang'],request.form['nlang'])
    if x==1:
        return render_template("login.html",message="account successfully created")
    if x==2:
        return render_template("register.html",message="invalid character in username")
    if x==3:
        return render_template("register.html",message="password too short")
    if x==4:
        return render_template("register.html",message="username already in use")
    if x==5:
        return render_template("register.html",message="passwords do not match")



if __name__ == "__main__":
    app.debug = True
    app.run()
