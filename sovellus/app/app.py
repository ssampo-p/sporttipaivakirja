import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, url_for, abort, flash
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
        password_hash = generate_password_hash(password1)
        try:
            db = Database()
            db.add_user(username, password_hash)
            db.close()
        except sqlite3.IntegrityError:
            flash("VIRHE: Valitsemasi tunnus on jo varattu")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
        return redirect("/")
    

@app.route("/user_page/<int:user_id>")
def own_page(user_id):
    ''' User's own page , can be accessed only when logged in '''
    if user_id != session["user_id"]:
        return abort(403)
    user_id = session["username"]
    username = session["username"]
    try:
        db = Database()
        workouts_from_db = db.get_workouts_by_user(session["user_id"])
        workouts = []
        if not workouts_from_db:
            return render_template("user_page.html",user_id=user_id, username=username, workouts=workouts)
        
        for workout in workouts_from_db:  
            workouts.append(Workout(workout[0], workout[1], workout[2], workout[3],workout[4], workout[5], session["user_id"], session["username"]))
            
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
    sport = request.form["workout_type"]
    
    try:
        db = Database()
        db.add_workout(content, sent_at, user_id, title, workout_level, sport)
        db.close()
        print(f"New workout post by user_id {user_id}: {content} at {sent_at} with title {title}, level {workout_level}")
        return redirect("/")
    except Exception as e:
        return f"error: {e}"
    
    
@app.route("/workouts")
def workouts():
    ''' Page showing all workout posts '''
    db = Database()
    workouts_from_db = db.get_workouts()
    workouts = []
    print(workouts_from_db)
    
    if not workouts_from_db:
        db.close()
        return render_template("workouts.html", workouts=workouts)
    
    create_workouts(db,workouts_from_db, workouts)
    # for workout in workouts_from_db:
    #     comments_from_db = db.get_workout_comments(workout[0])  
    #     workouts.append(Workout(
    #         workout[0],
    #         workout[1],
    #         workout[2],
    #         workout[3],
    #         workout[4],
    #         workout[5],
    #         db.get_username_by_id(workout[5]),
    #         comments_from_db
    #         ))
        
        
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

@app.route("/edit_workout/<int:workout_id>/<int:workout_user_id>", methods=["POST", "GET"])
def edit_workout(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
        
    
    print(workout_user_id)
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
            workout_from_db[6],
            db.get_username_by_id(workout_from_db[6]))
    db.close()
    
    if request.method == "POST":
        return render_template("edit_workout.html", workout = workout)
    if request.method == "GET":
        return render_template("edit_workout.html",workout = workout)
   
 
@app.route("/update_workout/<int:workout_id>/<int:workout_user_id>", methods=["POST"])
def update_workout(workout_id, workout_user_id):
    
    db  = Database()
    workout = db.get_workout(workout_id)
    if not workout or workout_user_id != session["user_id"]:
        db.close()
        abort(403)
    title = request.form["title"]
    new_content = request.form["content"]
    workout_level = request.form["workout_level"]
    sport = request.form["workout_type"]
    print("sport: ", sport)
    
    db.edit_workout(title, new_content, workout_level,sport, workout_id, session["user_id"])
    db.close 
    
    return redirect(url_for("own_page", user_id=session["user_id"])) 
    
@app.route("/workouts/sort_workouts", methods=["POST"])
def sort_workouts():
    workout_level = request.form["workout_level"]
    if workout_level == "all":
        return redirect(url_for("workouts",))
    db = Database()
    workouts_from_db = db.get_workouts_by_level(workout_level)
    workouts = []
    create_workouts(db, workouts_from_db, workouts)
    db.close()
        
    return render_template("workouts.html",workouts=workouts)

def create_workouts(db, workouts_from_db, workouts):
    for workout in workouts_from_db:
        comments_from_db = db.get_workout_comments(workout[0]) 
        workouts.append(Workout(workout[0],
                                workout[1],
                                workout[2],
                                workout[3],
                                workout[4],
                                workout[5],
                                workout[6],
                                db.get_username_by_id(workout[6]),
                                comments_from_db,
                                ))


@app.route("/delete_workout/<int:workout_id>/<int:workout_user_id>",methods=["POST"])
def delete_workout(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
        
    db = Database()
    db.delete_workout(workout_id)
    db.close()
    return redirect(url_for("own_page", user_id=session["user_id"]))
    
    