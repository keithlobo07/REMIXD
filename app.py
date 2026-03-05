from flask import Flask, jsonify
from flaskext import mysql
import requests, json

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get('https://www.theaudiodb.com/api/v1/json/123/searchalbum.php?s=daft_punk')
    if response.status_code == 200:
        data = response.json()
        print(data['album'][00]['strAlbum'])
    return data['album'][00]['strAlbum']

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
    return jsonify({
        "id":"1",
        "name":"Rose",
        "bio":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec est felis, facilisis fringilla rhoncus eu, posuere et neque. Nam at massa sodales tortor placerat convallis sed euismod erat. Vestibulum euismod ipsum ut justo finibus scelerisque. Fusce dapibus pulvinar turpis ac tristique. Nulla vehicula urna eu dui congue, id sollicitudin augue auctor. Curabitur interdum ultricies urna, nec mattis massa lobortis vitae. Etiam quis facilisis purus. Suspendisse nec sagittis libero.",
        "reviews":[
            {"rating":"10", "datetime":"1772451614", "flags":"011", "content":"I really like this album a whole lot."}
        ]
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)