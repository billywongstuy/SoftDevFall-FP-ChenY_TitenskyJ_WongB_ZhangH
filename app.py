from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, hashlib, os, utils
from utils import auth, posts, topic

app = Flask(__name__)
app.secret_key=os.urandom(32)

@app.route("/")
def home():
    if 'username' in session:
        return render_template("home.html",posts=topic.displayPosts())
    return render_template("login.html",message="")


@app.route("/login", methods=['POST'])
def login():
    password = hashlib.sha256(request.form['pw'])
    x=auth.userLogin(request.form['username'],password.hexdigest())
    if x[0]=='True':
        session['username'] = request.form['username']
        return redirect("/")
    if x[0]=='False':
        return render_template("login.html",message=x[1])

@app.route("/register")
def register():
   return render_template("register.html")

@app.route("/createAccount", methods=['POST'])
#routing is still messed up
def createAccount():
    if (request.form['plang2'] == None):
        plangs = request.form['plang1']
    else:
        plangs = request.form['plang1'] + "," + request.form['plang2']
    x=auth.addUser(request.form['username'],request.form['pw'],request.form['pwc'],plangs,request.form['nlang'])
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

@app.route("/logout")
def logout():
    session.pop('username')
    return render_template("login.html",message="logged out")

@app.route("/post")
def post():
    return render_template("test.html")

@app.route("/account")
def account():
    return render_template("test.html")

@app.route("/createPost")
def createPost():
    return render_template("writePost.html")

@app.route("/writePost",methods=['POST'])
def writePost():
    posts.addPost(session['username'],request.form['title'],request.form['words'],request.form['postLang'])
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
