from flask import Flask, jsonify, request
from flaskext.mysql import MySQL


app = Flask(__name__)
sql = MySQL(app)

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
    cursor.execute("SELECT Account.ID, Account.Name, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE AlbumID=%s ORDER BY Likes DESC LIMIT %s;", (albumid, limit))
    results = cursor.fetchall()
    cursor.close()

    return jsonify({
        "reviews":[{"id":x[0], "name":x[1], "timestamp":x[2], "score":x[3], "liked":x[4], "content":x[5], "numLikes":x[6], "userliked":False, "userreport":False} for x in results]
    })

@app.route("/api/user/<userid>")
def user_lookup(userid):
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT * FROM Account WHERE ID=%s LIMIT 1;",  str(userid))
    user = cursor.fetchone()
    cursor.execute("SELECT Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE Review.AccountID=%s ORDER BY Review.timestamp DESC LIMIT 5;", (userid))
    reviews = cursor.fetchall()
    cursor.close()
    
    return jsonify({
        "id":user[0],
        "name":user[1],
        "bio":user[5],
        "reviews":[{"albumid":x[0], "timestamp":x[1], "score":x[2], "liked":x[3], "content":x[4], "numLikes":x[5], "userliked":False, "userflagged":False} for x in reviews]
    })

@app.route("/api/albums")
def album_search():
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

if __name__ == "__main__":
    app.run()