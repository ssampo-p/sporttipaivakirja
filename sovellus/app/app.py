import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Database
from . import config
from datetime import datetime


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def sivu1():
    db = Database()
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    try:
        db = Database()
        user = db.get_user_by_id(username)
        if user and check_password_hash(user[2], password):
            session["username"] = username
            session["user_id"] = user[0]
            return redirect("/")
            
        else:
            return "Virheellinen käyttäjätunnus tai salasana"
    except Exception as e:
        return f"Tapahtui virhe: {e}"
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        db = Database()
        db.add_user(username, password_hash)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/user_page")
def own_page():
    ''' User's own page , can be accessed only when logged in '''
    if "username" not in session:
        return redirect("/")
    username = session["username"]
    return render_template("user_page.html", username=username)

@app.route("/new_workout_post", methods=["POST"])
def new_workout_post():
    ''' Create a new workout post '''
    if "user_id" not in session:
        return redirect("/")
    
    content = request.form["content"]
    user_id = session["user_id"]
    sent_at = datetime.now()
    title = request.form["title"]
    workout_level = request.form["workout_level"]
    
    try:
        db = Database()
        db.add_message(content, sent_at, user_id, title, workout_level)
    
        print(f"New workout post by user_id {user_id}: {content} at {sent_at} with title {title}, level {workout_level}")
        return redirect("/")
    except Exception as e:
        return f"error: {e}"