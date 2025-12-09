import sqlite3, secrets
from flask import Flask
from flask import redirect, render_template, request, session, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
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


@app.route("/")
def sivu1():
    db = Database()
    db.close()
    return render_template("index.html")
    

    

    

