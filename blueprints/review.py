from flask import *
from app import sql

reviews = Blueprint('reviews', __name__)

@reviews.route("/api/review/<userid>/<albumid>")
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
    
@reviews.post("/api/review")
def post_review():
    if not 'id' in session:
        return {"message": "not logged in"}, 409
    
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT modTags FROM Account WHERE ID = %s;" %session['id'])
    result = cursor.fetchone()[0]
    if result & 1:
        return {"message": "account banned from posting reviews"}, 409

    ID, score, content = request.form['id'], request.form['score'], request.form['content']

    # finish when bethany finishes review page

@reviews.put("/api/review")
def update_review():
    if not 'id' in session:
        return {"message": "not logged in"}, 409

    cursor = sql.get_db().cursor()
    cursor.execute("SELECT modTags FROM Account WHERE ID = %s;" %session['id'])
    result = cursor.fetchone()[0]
    if result & 1:
        return {"message": "account banned from posting reviews"}, 409
    
    ID, score, content = request.form['id'], request.form['score'], request.form['content']

    cursor.execute("UPDATE Review SET Score=%s, Content=%s WHERE ID = %s;", ID, score, content)

    # finish when bethany finishes review page
