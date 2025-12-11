import sqlite3, secrets
from flask import Flask, Blueprint
from flask import redirect, render_template, request, session, url_for, abort, flash
from database import Database
import config
from datetime import datetime
from workout import Workout
import markupsafe


def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


def check_empty_inputs(title, content, path):
    if not title.strip():
        flash("Postauksen täytyy sisältää otsikko !")
        return redirect(path)
    if not content.strip():
        flash("Postauksen täytyy sisältää viesti !") 
        return redirect(path)
    return None

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
        

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

# 3 functions because of pagination 
first_page = "Tämä on ensimmäinen sivu !"
last_page = "Tämä on viimeinen sivu !"
def check_page_num(page_num, page_count):
    if page_num < 1:
        flash(first_page)
        return redirect(f"/workouts/1")
    if page_num > page_count:
        flash(last_page)
        return redirect(f"/workouts/{page_count}")
    
def check_page_sort(page_num, page_count, workout_level, workout_type):
    if page_num < 1:
        flash(first_page)
        return redirect(url_for("workouts.sort_workouts",
                                workout_level=workout_level,
                                workout_type=workout_type,
                                page_num=1))
    if page_num > page_count:
        flash(last_page)
        return redirect(url_for("workouts.sort_workouts",
                                workout_level=workout_level,
                                workout_type=workout_type,
                                page_num=page_count))
def check_page_sort_query(page_num, page_count, query):
    if page_num < 1:
        flash(first_page)
        return redirect(url_for("workouts.sort_with_query",
                                sort_query=query,
                                page_num=1))
    if page_num > page_count:
        flash(last_page)
        return redirect(url_for("workouts.sort_with_query",
                                sort_query=query,
                                page_num=page_count))