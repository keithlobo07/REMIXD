from flask import *
from app import sql
from album import album_search_data

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


@pages.route("/albumView")
def album_view():
    album = {
        "albumArt": "https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg",
        "avgRating": "4.23",
        "idAlbum": "2130752",
        "intYearReleased": "2012",
        "numReviews":    "46071",
        "strAlbum": "good kid, m.A.A.d city",
        "strArtist": "Kendrick Lamar",
        "strGenre": "Hip-Hop",
        "tracklist": [
        "Sherane a.k.a. Master Splinter's Daughter",
        "Bitch, Don't Kill My Vibe",
        "Backseat Freestyle",
        "The Art of Peer Pressure",
        "Money Trees",
        "Poetic Justice",
        "good kid",
        "m.A.A.d city",
        "Swimming Pools (Drank) (extended version)",
        "Sing About Me, I'm Dying of Thirst",
        "Real",
        "Compton",
        "The Recipe",
        "Black Boy Fly",
        "Now or Never"
        ]}
    data = {"accountID":1,"albumID":2130752,"content":"still only like the third best kendrick lamar album lol","liked":1,"numLikes":0,"score":10,"timestamp":"Tue, 07 Apr 2026 14:39:47 GMT","user_liked":0,"user_report":0}

    albums = [album]
    datas = [data]
    return render_template("albumView.html", albums = albums, datas = datas)
  
@pages.route("/home")
def home():
    albums = album_search_data()['albums']
    print(albums)
    return render_template("allAlbumView.html", albums=albums)

@pages.route("/admin")
def admin_page():
    return render_template("adminDashboard.html"), 200