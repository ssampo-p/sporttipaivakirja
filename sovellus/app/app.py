import time
from flask import Flask, g, render_template
from database import Database
import config
from utils import show_lines
from workout_routes import workouts_bp
from user_routes import users_bp



app = Flask(__name__)
app.secret_key = config.SECRET_KEY
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
    return render_template("index.html", filled={})

@app.errorhandler(403)
def forbidden(_):
    return render_template("403.html"), 403
