import sqlite3, secrets
from flask import Flask
from flask import redirect, render_template, request, session, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
import config
from datetime import datetime
from workout import Workout
import utils 
from workout_routes import workouts_bp
from user_routes import users_bp




#TODO: distribute the code in this file to other files as the app grows larger
#TODO: add error handling where missing
#TODO: add pagination to workouts page
#TODO: add ability to delete comments
#TODO: add timestamps to comments


app = Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(workouts_bp)
app.register_blueprint(users_bp)


@app.route("/")
def sivu1():
    db = Database()
    db.close()
    return render_template("index.html")
    

    

    

