import sqlite3, secrets
from flask import Flask, Blueprint
from flask import redirect, render_template, request, session, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
import config
from datetime import datetime
from workout import Workout
import utils 

users_bp = Blueprint('users', __name__)
@users_bp.route("/login", methods=["POST"])
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
    

@users_bp.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")


@users_bp.route("/register", methods=["GET", "POST"])
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
    

@users_bp.route("/user_page/<int:user_id>")
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
    
