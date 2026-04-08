from flask import *
from app import sql

pages = Blueprint('pages', __name__)

@pages.route("/")
def lander():
    if 'id' in session:
        return redirect(url_for('pages.home')), 303 # = See Other (redirect w/ get)
    return render_template("lander.html"), 200 # = OK

@pages.route("/home")
def home():
    return render_template("allAlbumView.html"), 200 # = OK

@pages.route("/login")
def login_page():
    if 'id' in session:
        return redirect(url_for("pages.home")), 303 # = See Other (redirect w/ get)
    return render_template("login.html"), 200 # = OK

@pages.route("/signup")
def signup_page():
    if 'id' in session:
        return redirect(url_for("pages.home")), 303 # = See Other (redirect w/ get)
    return render_template("signup.html"), 200 # = OK