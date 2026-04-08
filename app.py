from flask import *
from flaskext.mysql import MySQL
from argon2 import PasswordHasher
import sys

sys.path.insert(0, "./blueprints")


app = Flask(__name__)
sql = MySQL(app)
ph = PasswordHasher()

app.secret_key = "cf39da25450430eb49098ec3f99b19cb4977a00355dbfd822a46626c262e1179"

app.config["MYSQL_DATABASE_HOST"] = "remixd.csumcw23kuop.us-east-1.rds.amazonaws.com"
app.config["MYSQL_DATABASE_USER"] = "admin"
app.config["MYSQL_DATABASE_PASSWORD"] = "O75BmgKdl9ZPnacoEwwQ"
app.config["MYSQL_DATABASE_DB"] = "remixd"

@app.route("/")
def lander():
    if 'id' in session:
        return redirect(url_for('home')), 303 # = See Other (redirect w/ get)
    return render_template("lander.html"), 200 # = OK

@app.route("/home")
def home():
    return render_template("allAlbumView.html"), 200 # = OK

@app.route("/api/session")
def session_check():
    # use this to check if you are logged in
    [print(x, session[x]) for x in session]

    if 'id' in session:
        return {"message": "logged in as %d" %session['id']}, 200 # = OK
    return {"message": "not logged in"}, 200 # = OK

@app.route("/login")
def login_page():
    if 'id' in session:
        return redirect(url_for("home")), 303 # = See Other (redirect w/ get)
    return render_template("login.html"), 200 # = OK

@app.route("/signup")
def signup_page():
    if 'id' in session:
        return redirect(url_for("home")), 303 # = See Other (redirect w/ get)
    return render_template("signup.html"), 200 # = OK


if __name__ == "__main__":
    from blueprints.user import users
    from blueprints.album import albums
    from blueprints.review import reviews
    from blueprints.admin import admins
    from blueprints.util import utils

    app.register_blueprint(users)
    app.register_blueprint(albums)
    app.register_blueprint(reviews)
    app.register_blueprint(admins)
    app.register_blueprint(utils)

    app.run(ssl_context='adhoc')