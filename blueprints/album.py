from flask import *
#from app import sql
import musicbrainzngs as mb
albums = Blueprint('albums', __name__)

mb.set_useragent("REMIXD", "0.8", "2644463@dundee.ac.uk")
mb.set_rate_limit(1)

trimmedData = {}

def album_lookup_data(albumid):
    #release group - d706457-8b16-4809-a61a-cdba1b281d39 - brand new eyes paramore
    #release 11755c21-2546-4cb3-9b87-392f4f3c2fa2 - ten the story - twice

    response = mb.get_release_by_id(albumid, includes=["recordings", "artists", "tags"])
    responseData = response['release']

    trackListData = responseData['medium-list'][0]['track-list']
    trimmedTrackList = []
    for elements in trackListData:
        trackData = {
            "trackNumber":elements["number"],
            "name":elements["recording"]["title"],
            "length":elements["recording"]["length"]
        }
        trimmedTrackList.append(trackData)

    trimmedData = {
        "idAlbum" : responseData['id'],
        "albumName" : responseData["title"],
        "artist" : responseData["artist-credit-phrase"],
        "releaseDate" : responseData["date"],
        "coverArt" : mb.get_image_list(albumid)['images'][00]['image'],
        "trackList":trimmedTrackList
    }

    return trimmedData



@albums.get("/api/album/<albumid>")
def album_lookup(albumid):
    data = album_lookup_data(albumid)
    if data == None:
        return {"message":"Album %s could not be found." %albumid}, 404 # = Not Found
    return jsonify(data), 200 # = OK

def album_review_info(albumid):
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT COUNT(*), AVG(Score) FROM Review WHERE AlbumID = %s;", albumid)
    reviews, avg_score = cursor.fetchone()[0]
    cursor.close()

    return {"numReviews":reviews, "avgScore":avg_score}


@albums.get("/api/album/<albumid>/reviews")
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

def album_search_data(query):
    responseData = mb.search_release_groups(query) # type: ignore
    searchResults = []
    for elements in responseData['release-group-list']:
        trimmedAlbumData = {
            "idAlbum" : elements['id'],
            "albumName" : elements["title"],
            "artist" : elements["artist-credit-phrase"],
            "releaseDate" : elements["first-release-date"]
        }
        searchResults.append(trimmedAlbumData)

    return searchResults

@albums.route("/api/album/search")
def album_search():
    query = request.args.get("query", type=str)
    if query == None:
        return {"message": "No query phrase provided."}, 400 # = Bad Request

    data = album_search_data(query)

    if data == None:
        return {"message":"Album search returned no data."}, 404 # = Not Found
    return jsonify(data), 200