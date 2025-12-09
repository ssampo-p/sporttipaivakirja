import sqlite3, secrets
from flask import Flask, Blueprint
from flask import redirect, render_template, request, session, url_for, abort, flash
from database import Database
import config
from datetime import datetime
from workout import Workout
import utils 
from math import ceil

workouts_bp = Blueprint('workouts', __name__)

@workouts_bp.route("/new_workout_post", methods=["POST"])
def new_workout_post():
    ''' Create a new workout post '''
    if "user_id" not in session:
        return redirect("/")
    utils.check_csrf() 
    content = request.form["content"]
    user_id = session["user_id"]
    sent_at = datetime.now().isoformat(" ")
    title = request.form["title"]
    workout_level = request.form["workout_level"]
    sport = request.form["workout_type"]
    check = utils.check_empty_inputs(title, content, "/")
    if check:
        return check
    if not title or len(title) > 100 or len(content) > 5000:
        abort(403)
    try:
        db = Database()
        db.add_workout(content, sent_at, user_id, title, workout_level, sport)
        db.close()
        flash("Uusi suorituksesi on tallennettu!")
        return redirect("/")
    except sqlite3.IntegrityError as e:
        flash("VIRHE: suoritusta ei voitu tallentaa")
        return redirect("/")
    finally:
        db.close

@workouts_bp.route("/workouts")
def workouts_redirect():
    return redirect("/workouts/1")
    
@workouts_bp.route("/workouts/<int:page_num>")
def workouts(page_num):
    page_size = 2
    db = Database()

    workout_count = db.get_workout_count()
    page_count = max(ceil(workout_count / page_size), 1)
    
    if page_num < 1:
        flash("Tämä on ensimmäinen sivu !")
        return redirect("/workouts/1")
    if page_num > page_count:
        flash("Tämä on viimeinen sivu !")
        return redirect(f"/workouts/{page_count}")
    
    workouts_from_db = db.get_workouts_w_page(page_num, page_size)

    workouts = []
    if not workouts_from_db:
        db.close()
        return render_template("workouts.html", workouts=workouts, page_num=page_num, page_count=page_count)

    utils.create_workouts(db, workouts_from_db, workouts)
    db.close()

    return render_template("workouts.html", workouts=workouts, page_num=page_num, page_count=page_count)


@workouts_bp.route("/comment_post/<int:workout_id>", methods=["POST"])
def comment_post(workout_id):
    ''' Creates a new comment on a workout post '''
    if "user_id" not in session:
        return redirect("/")
    utils.check_csrf()
    comment_content = request.form["comment_content"]
    if not comment_content.strip() or len(comment_content) > 500:
        flash("Et voi lähettää tyhjää kommenttia!")
        return redirect(url_for("workouts.workouts"))
    db = Database()
    db.add_comment_to_workout(workout_id, session["user_id"], comment_content)
    db.close()
    return redirect("/workouts")

@workouts_bp.route("/edit_workout/<int:workout_id>/<int:workout_user_id>", methods=["POST", "GET"])
def edit_workout(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
    if request.method == "POST": # to show the edit form if check_empty_inputs fails
        utils.check_csrf()
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
   
 
@workouts_bp.route("/update_workout/<int:workout_id>/<int:workout_user_id>", methods=["POST"])
def update_workout(workout_id, workout_user_id):
    utils.check_csrf()
    db  = Database()
    workout = db.get_workout(workout_id)
    if not workout or workout_user_id != session["user_id"]:
        db.close()
        abort(403)
    title = request.form["title"]
    new_content = request.form["content"]
    workout_level = request.form["workout_level"]
    sport = request.form["workout_type"]
    check = utils.check_empty_inputs(title, new_content, url_for("workouts.edit_workout", workout_id=workout_id, workout_user_id=workout_user_id))
    if check:
        return check
    db.edit_workout(title, new_content, workout_level,sport, workout_id, session["user_id"])
    db.close() 
    
    return redirect(url_for("users.own_page", user_id=session["user_id"])) 


     
@workouts_bp.route("/workouts/sort_workouts", methods=["GET"])
def sort_workouts():
    workout_level = request.args.get("workout_level")
    sport = request.args.get("workout_type")
    if workout_level == "all" and sport == "all":
        return redirect(url_for("workouts.workouts",page_num=1))
    db = Database()
    workouts_from_db = db.get_sorted_workouts(workout_level, sport)
    workouts = []
    utils.create_workouts(db, workouts_from_db, workouts)
    db.close()
        
    return render_template("workouts.html",workouts=workouts, page_num=1, page_count=1)

@workouts_bp.route("/workouts/search", methods=["POST","GET"])
def sort_with_query():
    if request.method == "POST":
        query = request.form["sort_query"]
        return redirect(url_for("workouts.sort_with_query", sort_query=query))
        
    query = request.args["sort_query"]
    
    if query == "":
        return redirect(url_for("workouts.workouts", page_num=1))
    db = Database()
    workouts_from_db = db.sort_workouts_query(query)
    workouts = []
    utils.create_workouts(db, workouts_from_db, workouts)
    db.close()
    
    return render_template("workouts.html", workouts=workouts ,query = query, page_num=1, page_count=1)
    
    


@workouts_bp.route("/delete_workout/<int:workout_id>/<int:workout_user_id>",methods=["POST"])
def delete_workout(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
    utils.check_csrf()
    db = Database()
    db.delete_comments(workout_id)
    db.delete_workout(workout_id)
    db.close()
    return redirect(url_for("users.own_page", user_id=session["user_id"]))

@workouts_bp.route("/delete_workout/confirmation/<int:workout_id>/<int:workout_user_id>/",methods=["POST"])
def delete_workout_confirmation(workout_id, workout_user_id):
    if workout_user_id != session["user_id"]:
        abort(403)
    utils.check_csrf()
    return render_template("delete_workout.html", workout_id=workout_id, workout_user_id=workout_user_id)



