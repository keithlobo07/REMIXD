from flask import *
from app import sql
from album import album_search_data, album_lookup_data
from admin import is_admin, admin_review_count
from user import user_data

pages = Blueprint('pages', __name__)

@pages.route("/")
def lander():
    if 'id' in session:
        return redirect(url_for('pages.home')), 303 # = See Other (redirect w/ get)
    return render_template("lander.html"), 200 # = OK

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


@pages.route("/user/<userid>")
def user_page(userid):
    return render_template("userView.html", user=user_data(userid), ownprofile=int(userid)==session['id'])


@pages.route("/album/<albumid>")
def album_view(albumid):
    album = album_lookup_data(albumid)
    return render_template("albumView.html", album = album)
  
@pages.route("/home")
def home():
    albums = album_search_data("riot!")
    print(albums)
    return render_template("allAlbumView.html", albums=albums)

@pages.route("/admin")
def admin_page():
    if not is_admin():
        return {"message":"Insufficient permissions."}, 401 # = Unauthorized
    print(admin_review_count())
    return render_template("adminDashboard.html", toReview=admin_review_count()), 200