import sqlite3, secrets
from flask import Flask
from flask import redirect, render_template, request, session, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
import config
from datetime import datetime
from workout import Workout
import utils 


#TODO: distribute the code in this file to other files as the app grows larger
#TODO: add error handling where missing
#TODO: add pagination to workouts page
#TODO: add ability to delete comments
#TODO: add timestamps to comments


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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
            
        else:
            flash("Väärä käyttäjätunnus tai salasana")
            return redirect("/")
    except sqlite3.IntegrityError as e:
        return f"Tapahtui virhe: {e}"
    finally:
        redirect("/")
    

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
        if len(username) > 16: # should not happen
            flash("VIRHE: tunnus liian pitkä!")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        if not password1.strip():
            flash("VIRHE: salasana ei voi olla tyhjä!")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

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
        finally:
            if db:
                db.close()

        flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
        return redirect("/")
    

@app.route("/user_page/<int:user_id>")
def own_page(user_id):
    ''' User's own page , can be accessed only when logged in '''
    if user_id != session["user_id"]:
        return abort(403)
    username = session["username"]
    try:
        db = Database()
        workouts_from_db = db.get_workouts_by_user(session["user_id"])
        workouts = []
        if not workouts_from_db:
            weekly_count = 0
            thirty_days_count = 0
            db.close()
            return render_template("user_page.html",user_id=user_id, username=username, workouts=workouts, weekly_count=weekly_count, thirty_days_count=thirty_days_count)
        
        for workout in workouts_from_db:
            comments_from_db = db.get_workout_comments(workout[0])  
            workouts.append(Workout(workout[0],
                                    workout[1],
                                    workout[2],
                                    workout[3],
                                    workout[4],
                                    workout[5],
                                    session["user_id"],
                                    session["username"],
                                    comments_from_db,
                                    ))
        weekly_count = db.get_workouts_count(user_id,"week")
        thirty_days_count = db.get_workouts_count(user_id, "30days") 
        db.close()
        return render_template("user_page.html",user_id=user_id, username=username, workouts=workouts, weekly_count=weekly_count, thirty_days_count=thirty_days_count)
    except sqlite3.IntegrityError as e:
        flash("Tapahtui virhe oman sivun lataamisessa!")
    finally:
        if db:
            db.close()
    

@app.route("/new_workout_post", methods=["POST"])
def new_workout_post():
    ''' Create a new workout post '''
    if "user_id" not in session:
        return redirect("/")
    check_csrf() 
    content = request.form["content"]
    user_id = session["user_id"]
    sent_at = datetime.now().isoformat(" ")
    title = request.form["title"]
    workout_level = request.form["workout_level"]
    sport = request.form["workout_type"]
    check = check_empty_inputs(title, content, "/")
    if check:
        return check
    if not title or len(title) > 100 or len(content) > 5000:
        abort(403)
    try:
        db = Database()
        db.add_workout(content, sent_at, user_id, title, workout_level, sport)
        db.close()
        return redirect("/")
    except sqlite3.IntegrityError as e:
        flash("VIRHE: suoritusta ei voitu tallentaa")
        return redirect("/")
    finally:
        db.close
    
    
@app.route("/workouts")
def workouts():
    ''' Page showing all workout posts '''
    db = Database()
    workouts_from_db = db.get_workouts()
    workouts = []
    if not workouts_from_db:
        db.close()
        return render_template("workouts.html", workouts=workouts)  
    create_workouts(db,workouts_from_db, workouts)        
    db.close()
    return render_template("workouts.html", workouts=workouts)

@app.route("/comment_post/<int:workout_id>", methods=["POST"])
def comment_post(workout_id):
    ''' Creates a new comment on a workout post '''
    if "user_id" not in session:
        return redirect("/")
    check_csrf()
    comment_content = request.form["comment_content"]
    if not comment_content.strip() or len(comment_content) > 500:
        flash("Et voi lähettää tyhjää kommenttia!")
        return redirect(url_for("workouts"))
    db = Database()
    db.add_comment_to_workout(workout_id, session["user_id"], comment_content)
    db.close()
    return redirect("/workouts")

@app.route("/edit_workout/<int:workout_id>/<int:workout_user_id>", methods=["POST", "GET"])
def edit_workout(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
    check_csrf()
    db = Database()
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
    check_csrf()
    db  = Database()
    workout = db.get_workout(workout_id)
    if not workout or workout_user_id != session["user_id"]:
        db.close()
        abort(403)
    title = request.form["title"]
    new_content = request.form["content"]
    workout_level = request.form["workout_level"]
    sport = request.form["workout_type"]
    check = check_empty_inputs(title, new_content, url_for("edit_workout", workout_id=workout_id, workout_user_id=workout_user_id))
    if check:
        return check
    db.edit_workout(title, new_content, workout_level,sport, workout_id, session["user_id"])
    db.close 
    
    return redirect(url_for("own_page", user_id=session["user_id"])) 



def check_empty_inputs(title, content, path):
    if not title.strip():
        flash("Postauksen täytyy sisältää otsikko !")
        return redirect(path)
    if not content.strip():
        flash("Postauksen täytyy sisältää viesti !") 
        return redirect(path)
    return None
     
@app.route("/workouts/sort_workouts", methods=["GET"])
def sort_workouts():
    workout_level = request.args.get("workout_level")
    sport = request.args.get("workout_type")
    if workout_level == "all" and sport == "all":
        return redirect(url_for("workouts",))
    db = Database()
    workouts_from_db = db.get_sorted_workouts(workout_level, sport)
    workouts = []
    create_workouts(db, workouts_from_db, workouts)
    db.close()
        
    return render_template("workouts.html",workouts=workouts)

@app.route("/workouts/search", methods=["POST","GET"])
def sort_with_query():
    if request.method == "POST":
        query = request.form["sort_query"]
        return redirect(url_for("sort_with_query", sort_query=query))
        
    query = request.args["sort_query"]
    
    if query == "":
        return redirect(url_for("workouts",))
    db = Database()
    workouts_from_db = db.sort_workouts_query(query)
    workouts = []
    create_workouts(db, workouts_from_db, workouts)
    db.close()
    
    return render_template("workouts.html", workouts=workouts ,query = query)
    
    
    
        
        

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
    check_csrf()
    db = Database()
    db.delete_workout(workout_id)
    db.close()
    return redirect(url_for("own_page", user_id=session["user_id"]))

@app.route("/delete_workout/confirmation/<int:workout_id>/<int:workout_user_id>/",methods=["POST"])
def delete_workout_confirmation(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
    check_csrf()
    return render_template("delete_workout.html", workout_id=workout_id, workout_user_id=workout_user_id)




def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    

