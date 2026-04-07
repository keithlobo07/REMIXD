from flask import *
from flaskext.mysql import MySQL
from argon2 import PasswordHasher


app = Flask(__name__)
sql = MySQL(app)
ph = PasswordHasher()

app.secret_key = "cf39da25450430eb49098ec3f99b19cb4977a00355dbfd822a46626c262e1179"

app.config["MYSQL_DATABASE_HOST"] = "remixd.csumcw23kuop.us-east-1.rds.amazonaws.com"
app.config["MYSQL_DATABASE_USER"] = "admin"
app.config["MYSQL_DATABASE_PASSWORD"] = "O75BmgKdl9ZPnacoEwwQ"
app.config["MYSQL_DATABASE_DB"] = "remixd"

@app.route("/api/album/<albumid>")
def album_lookup(albumid):
    return jsonify({
        "idAlbum":"2130752",
        "strAlbum":"good kid, m.A.A.d city",
        "strArtist":"Kendrick Lamar",
        "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg",
        "intYearReleased":"2012",
        "strGenre":"Hip-Hop",
        "avgRating":"4.23",
        "numReviews":"46071",
        "tracklist":[
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
        ]})

@app.route("/api/album/<albumid>/reviews")
def albums_reviews(albumid):
    limit = request.args.get('limit')
    limit = int(limit) if limit != None else 5

    cursor = sql.get_db().cursor()

    if 'id' in session:
        # user is logged in -> get perspective data 
        cursor.execute("SELECT Account.ID, Account.Name, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, IFNULL(Tags.info & 128 = 128, 0) as user_like, IFNULL(Tags.info & 64 = 64, 0) as user_report FROM Review JOIN Account ON Account.ID = Review.AccountID LEFT JOIN Tags ON Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.AccountID = %s WHERE AlbumID=%s ORDER BY Likes DESC LIMIT %s;", (session['id'], albumid, limit))
        results = cursor.fetchall()

        cursor.close()

        return jsonify({
            "reviews":[{"id":x[0], "name":x[1], "timestamp":x[2], "score":x[3], "liked":x[4], "content":x[5], "numLikes":x[6], "user_liked":x[7], "user_report":x[8]} for x in results]
        })
    else:
        # no login -> anonymous data
        cursor.execute("SELECT Account.ID, Account.Name, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE AlbumID=%s ORDER BY Likes DESC LIMIT %s;", (albumid, limit))
        results = cursor.fetchall()

        cursor.close()

        return jsonify({
            "reviews":[{"id":x[0], "name":x[1], "timestamp":x[2], "score":x[3], "liked":x[4], "content":x[5], "numLikes":x[6]} for x in results]
        })

@app.route("/api/user/<userid>")
def user_lookup(userid):
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT * FROM Account WHERE ID=%s LIMIT 1;",  str(userid))
    user = cursor.fetchone()
    if 'id' in session:
        # user is logged in -> perspective data
        cursor.execute("SELECT Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, IFNULL(Tags.info & 128 = 128, 0) as user_like, IFNULL(Tags.info & 64 = 64, 0) as user_report FROM Review JOIN Account ON Account.ID = Review.AccountID LEFT JOIN Tags ON Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.AccountID = %s WHERE Review.AccountID=%s ORDER BY Review.timestamp DESC LIMIT 5;", (session['id'], userid))
        reviews = cursor.fetchall()
        cursor.close()
        
        return jsonify({
            "id":user[0],
            "name":user[1],
            "bio":user[5],
            "reviews":[{"albumid":x[0], "timestamp":x[1], "score":x[2], "liked":x[3], "content":x[4], "numLikes":x[5], "user_liked":x[6], "user_flagged":x[7]} for x in reviews]
        })
    else:
        # no login -> anonymous data
        cursor.execute("SELECT Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE Review.AccountID=%s ORDER BY Review.timestamp DESC LIMIT 5;", (userid))
        reviews = cursor.fetchall()
        cursor.close()
        
        return jsonify({
            "id":user[0],
            "name":user[1],
            "bio":user[5],
            "reviews":[{"albumid":x[0], "timestamp":x[1], "score":x[2], "liked":x[3], "content":x[4], "numLikes":x[5], "user_liked":x[6], "user_report":x[7]} for x in reviews]
        })

@app.route("/api/albums")
def album_search():
    query = request.args.get("query")
    if query == None:
        return {"message": "no query phrase"}, 400 # = Bad Request

    return jsonify({
        "albums":[
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"}   
        ]
    })

@app.route("/api/review/<userid>/<albumid>")
def review_lookup(userid, albumid):
    cursor = sql.get_db().cursor()

    if 'id' in session:
        cursor.execute("SELECT Review.AccountID, Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, IFNULL(Tags.info & 128 = 128, 0) as user_like, IFNULL(Tags.info & 64 = 64, 0) as user_report FROM Review LEFT JOIN Tags ON Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.AccountID = %s WHERE Review.AccountID=%s AND AlbumID=%s;", (session['id'], userid, albumid))
        data = cursor.fetchone()
        cursor.close()

        return jsonify({
            "accountID":data[0],
            "albumID":data[1],
            "timestamp":data[2],
            "score":data[3],
            "liked":data[4],
            "content":data[5],
            "numLikes":data[6],
            "user_liked":data[7],
            "user_report":data[8]
        })
    else:
        cursor.execute("SELECT AccountID, AlbumID, timestamp, Score, Liked, Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review WHERE AccountID=%s AND AlbumID=%s;", (userid, albumid))
        data = cursor.fetchone()
        cursor.close()

        return jsonify({
            "accountID":data[0],
            "albumID":data[1],
            "timestamp":data[2],
            "score":data[3],
            "liked":data[4],
            "content":data[5],
            "numLikes":data[6]
        })

@app.route("/api/admin/reviews")
def admin_review_search():
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT *, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 64) AS Reports, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review ORDER BY Reports DESC LIMIT 5;")
    results = cursor.fetchall()
    cursor.close()

    return jsonify({
        "reviews":[{"accountID":x[0], "albumID":x[1], "timestamp":x[2], "score":x[3], "liked":x[4], "content":x[5], "reports":x[6], "likes":x[7]} for x in results]
    })

@app.route("/api/admin/users")
def admin_user_search():
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT ReviewAccountID, (SELECT Name FROM Account WHERE ID = Tags.ReviewAccountID) AS Name, COUNT(*) AS `Total Reports` FROM Tags WHERE info & 64 GROUP BY ReviewAccountID ORDER BY `Total Reports` LIMIT 5;")
    results = cursor.fetchall()
    cursor.close()

    return jsonify({
        "users":[{"accountID":x[0], "name":x[1], "numReports":x[2]} for x in results]
    })

@app.route("/api/admin/statistics")
def admin_stats():
    cursor = sql.get_db().cursor()
    cursor.execute()
    results = cursor.fetchone()
    cursor.close()

    return jsonify({
        "data":[]
    })

@app.post("/api/authenticate")
def authenticate():
    email = request.form['email']
    given_password = request.form['password']

    cursor = sql.get_db().cursor()
    cursor.execute("SELECT ID, Password FROM Account WHERE email = %s", (email))
    results = cursor.fetchone()
    
    if results != None:
        ID, password = results
        try:
            # throws an exception if the hash doesnt match
            ph.verify(password, given_password)
            session['id'] = ID

            # good practice to rehash passwords where necessary
            if (ph.check_needs_rehash(password)):
                cursor.execute("UPDATE Account SET Password = %s WHERE ID = %s;" %(ph.hash(given_password)), ID)
                sql.get_db().commit()
            cursor.close()

            return redirect(url_for("home")), 303 # = See Other (redirect w/ get)
        except:
            # password didnt match
            cursor.close()
            return redirect(url_for("login_page")), 403 # = Forbidden
    else: # email didnt match
        cursor.close()
        return redirect(url_for("login_page")), 403 # = Forbidden


@app.route("/api/logout")
def logout():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for("lander")), 303 # = See Other (redirect w/ get)

@app.put("/api/signup")
def signup():
    if not 'id' in session:
        email, password, username = request.form['email'], request.form['password'], request.form['username']
        
        cursor = sql.get_db().cursor()
        cursor.execute("SELECT Email FROM Account WHERE email = %s", (email))
        results = cursor.fetchone()

        if results == None:
            # no user with this email -> add to database and login
            cursor.execute("INSERT INTO Account (Name, Email, Password) VALUES (%s, %s, %s);", (username, email, ph.hash(password)))
            sql.get_db().commit()
            cursor.execute("SELECT ID FROM Account WHERE email = %s", email)
            r = cursor.fetchone()
            
            if r == None:
                # some messed up database connection error would have to happen to get here but ill account for it
                cursor.close()
                return {"message", "error occured when retreiving id from database"}, 500 # = Internal Server Error
            
            session['id'] = r[0]
            cursor.close()
            return redirect(url_for('home')), 201 # = Created
        else:
            # user with this email already exists
            cursor.close()
            return {"message": "email already exists"}, 409 # = Conflict
    else:
        return redirect(url_for('home')), 303 # = See Other (redirect w/ get)

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
    app.run(ssl_context='adhoc')