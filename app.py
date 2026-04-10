from platform import release
from turtle import title
from urllib import response

from flask import *
from flaskext.mysql import MySQL
from argon2 import PasswordHasher
import sys

sys.path.insert(1, "./blueprints")


app = Flask(__name__)
sql = MySQL(app)
ph = PasswordHasher()


app.secret_key = "cf39da25450430eb49098ec3f99b19cb4977a00355dbfd822a46626c262e1179"

app.config["MYSQL_DATABASE_HOST"] = "remixd.csumcw23kuop.us-east-1.rds.amazonaws.com"
app.config["MYSQL_DATABASE_USER"] = "admin"
app.config["MYSQL_DATABASE_PASSWORD"] = "O75BmgKdl9ZPnacoEwwQ"
app.config["MYSQL_DATABASE_DB"] = "remixd"

if __name__ == "__main__":
    from blueprints.user import users
    from blueprints.album import albums
    from blueprints.review import reviews
    from blueprints.admin import admins
    from blueprints.util import utils
    from blueprints.page import pages

    app.register_blueprint(users)
    app.register_blueprint(albums)
    app.register_blueprint(reviews)
    app.register_blueprint(admins)
    app.register_blueprint(utils)
    app.register_blueprint(pages)

    app.run(ssl_context='adhoc', host="0.0.0.0", port=80)