import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Database
from . import config
from datetime import datetime
from app.workout import Workout



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
    del session["user_id"]
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
        db.close()
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/user_page/<int:user_id>")
def own_page(user_id):
    ''' User's own page , can be accessed only when logged in '''
    if "username" not in session:
        return redirect("/")
    user_id = session["username"]
    username = session["username"]
    try:
        db = Database()
        workouts_from_db = db.get_workouts_by_user(session["user_id"])
        workouts = []
        if not workouts_from_db:
            return render_template("user_page.html",user_id=user_id, username=username, workouts=workouts)
        
        for workout in workouts_from_db:  
            workouts.append(Workout(workout[0], workout[1], workout[2], workout[3],workout[4], session["user_id"], session["username"]))
            
        db.close()
        return render_template("user_page.html",user_id=user_id, username=username, workouts=workouts)
    except Exception as e:
        return f"error: {e}"
    


@app.route("/new_workout_post", methods=["POST"])
def new_workout_post():
    ''' Create a new workout post '''
    if "user_id" not in session:
        return redirect("/")
    
    content = request.form["content"]
    user_id = session["user_id"]
    sent_at = datetime.now().isoformat(" ")
    title = request.form["title"]
    workout_level = request.form["workout_level"]
    
    try:
        db = Database()
        db.add_workout(content, sent_at, user_id, title, workout_level)
        db.close()
        print(f"New workout post by user_id {user_id}: {content} at {sent_at} with title {title}, level {workout_level}")
        return redirect("/")
    except Exception as e:
        return f"error: {e}"
    
    
@app.route("/workouts")
def workouts():
    ''' Page showing all workout posts '''
    if "user_id" not in session:
        return redirect("/")
    db = Database()
    workouts_from_db = db.get_workouts()
    workouts = []
    print(workouts_from_db)
    
    if not workouts_from_db:
        db.close()
        return render_template("workouts.html", workouts=workouts)
    
    
    for workout in workouts_from_db:
        comments_from_db = db.get_workout_comments(workout[0])  
        workouts.append(Workout(
            workout[0],
            workout[1],
            workout[2],
            workout[3],
            workout[4],
            workout[5],
            db.get_username_by_id(workout[5]),
            comments_from_db
            ))
        
        
    db.close()
    return render_template("workouts.html", workouts=workouts)

@app.route("/comment_post/<int:workout_id>", methods=["POST"])
def comment_post(workout_id):
    ''' Creates a new comment on a workout post '''
    if "user_id" not in session:
        return redirect("/")
    comment_content = request.form["comment_content"]
    db = Database()
    db.add_comment_to_workout(workout_id, session["user_id"], comment_content)
    db.close()
    return redirect("/workouts")

@app.route("/edit_workout/<int:workout_id>", methods=["POST"])
def edit_workout(workout_id):
    db = Database()
    print("workout_id", workout_id)
    workout_from_db = db.get_workout(workout_id)
    #TODO not the best way create workout obj..
    workout = Workout(workout_from_db[0],
            workout_from_db[1],
            workout_from_db[2],
            workout_from_db[3],
            workout_from_db[4],
            workout_from_db[5],
            db.get_username_by_id(workout_from_db[5]))
    
    
    if request.method == "POST":
        return render_template("edit_workout.html", workout = workout)
    db.close()
 
@app.route("/update_workout/<int:workout_id>", methods=["POST"])
def update_workout(workout_id):
    db  = Database()
    new_content = request.form["content"]
    workout_level = request.form["workout_level"]
    db.edit_workout(new_content, workout_level, workout_id, session["user_id"])
    db.close 
    
    return redirect(url_for("own_page", user_id=session["user_id"])) 
    