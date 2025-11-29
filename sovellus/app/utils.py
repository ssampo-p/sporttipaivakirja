import sqlite3, secrets
from flask import Flask, Blueprint
from flask import redirect, render_template, request, session, url_for, abort, flash
from database import Database
import config
from datetime import datetime
from workout import Workout


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