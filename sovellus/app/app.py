import sqlite3, secrets
from flask import Flask
from flask import redirect, render_template, request, session, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
import time
from flask import g
from database import Database
import config
from datetime import datetime
from workout import Workout
from utils import show_lines
from workout_routes import workouts_bp
from user_routes import users_bp



app = Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(workouts_bp)
app.register_blueprint(users_bp)
app.add_template_filter(show_lines)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response


@app.route("/")
def sivu1():
    db = Database()
    db.close()
    return render_template("index.html")
