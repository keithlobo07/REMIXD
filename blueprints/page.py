from flask import *
from app import sql
from album import album_search_data, album_lookup_data
from admin import is_admin, admin_review_count

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


@pages.route("/user")
def user_page():
    data = {"accountID":1,"albumID":2130752,"content":"still only like the third best kendrick lamar album lol","liked":1,"numLikes":0,"score":10,"timestamp":"Tue, 07 Apr 2026 14:39:47 GMT","user_liked":0,"user_report":0}

    datas = [data]
    return render_template("userView.html", datas = datas)

@pages.route("/ownUser")
def ownUser_page():
    data = {"accountID":1,"albumID":2130752,"content":"still only like the third best kendrick lamar album lol","liked":1,"numLikes":0,"score":10,"timestamp":"Tue, 07 Apr 2026 14:39:47 GMT","user_liked":0,"user_report":0}

    datas = [data]
    return render_template("ownUserView.html", datas = datas)


@pages.route("/album/<albumid>")
def album_view(albumid):
    album = album_lookup_data(albumid)
    return render_template("albumView.html", album = album)
  
@pages.route("/home")
def home():
    albums = album_search_data(" ")['albums']
    print(albums)
    return render_template("allAlbumView.html", albums=albums)

@pages.route("/admin")
def admin_page():
    if not is_admin():
        return {"message":"Insufficient permissions."}, 401 # = Unauthorized
    print(admin_review_count())
    return render_template("adminDashboard.html", toReview=admin_review_count()), 200