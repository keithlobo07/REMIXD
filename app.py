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
    return jsonify({
        "reviews":[
            {"id":"1", "name":"Rose", "rating":"10", "datetime":"1772451614", "flags":"011", "content":"I really like this album a whole lot."},
            {"id":"2", "name":"Imran", "rating":"1", "datetime":"1772451679", "flags":"100", "content":"I fucking hate this album and i hate all other good music as well."},
            {"id":"3", "name":"Bethany", "rating":"7", "datetime":"1772451785", "flags":"001", "content":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris vel tellus dictum, pellentesque mauris ut, posuere dui. Quisque tortor est, consectetur et magna eu, blandit porttitor nunc."},
            {"id":"4", "name":"Keith", "rating":"9", "datetime":"1772451958", "flags":"110", "content":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec dictum tortor at mauris aliquet imperdiet. Cras vitae tellus consectetur, imperdiet erat vel, pharetra lectus."}
        ]
    })

@app.route("/api/user/<userid>")
def user_lookup(userid):
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT * FROM Account WHERE ID=%s LIMIT 1;" %str(userid))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM Review WHERE AccountID=%d ORDER BY timestamp DESC LIMIT 5;" %user[0])
    reviews = cursor.fetchall()
    
    return jsonify({
        "id":user[0],
        "name":user[1],
        "bio":user[5],
        "reviews":[{"albumid":x[1], "timestamp":x[2], "score":x[3], "content":x[4], "flags":"000"} for x in reviews]
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

if __name__ == "__main__":
    app.run()