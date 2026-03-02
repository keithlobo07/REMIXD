from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/api/album/<albumid>")
def user(albumid):
    return jsonify({"idAlbum":"2130752",
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

if __name__ == "__main__":
    app.run()