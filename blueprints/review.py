from flask import *
from app import sql
from admin import is_admin
from user import is_banned

reviews = Blueprint('reviews', __name__)

def review_data(userid, albumid):
    cursor = sql.get_db().cursor()

    if 'id' in session:
        cursor.execute("SELECT Review.AccountID, Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, IFNULL(Tags.info & 128 = 128, 0) as user_like, IFNULL(Tags.info & 64 = 64, 0) as user_report FROM Review LEFT JOIN Tags ON Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.AccountID = %s WHERE Review.AccountID=%s AND AlbumID=%s;", (session['id'], userid, albumid))
        data = cursor.fetchone()
        cursor.close()

        return {
            "accountID":data[0],
            "albumID":data[1],
            "timestamp":data[2],
            "score":data[3],
            "liked":data[4],
            "content":data[5],
            "numLikes":data[6],
            "user_liked":data[7],
            "user_report":data[8]
        }
    else:
        cursor.execute("SELECT AccountID, AlbumID, timestamp, Score, Liked, Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review WHERE AccountID=%s AND AlbumID=%s;", (userid, albumid))
        data = cursor.fetchone()
        cursor.close()

        return {
            "accountID":data[0],
            "albumID":data[1],
            "timestamp":data[2],
            "score":data[3],
            "liked":data[4],
            "content":data[5],
            "numLikes":data[6]
        }

@reviews.get("/api/review/<userid>/<albumid>")
def review_lookup(userid, albumid):
    return jsonify(review_data(userid, albumid))
    
@reviews.post("/api/review")
def post_review():
    if not 'id' in session:
        return {"message": "not logged in"}, 400
    
    if is_banned():
        return {"message": "account banned from posting reviews"}, 403

    album_id, score, content = request.form['album_id'], request.form['score'], request.form['content']

    # finish when bethany finishes review page

@reviews.put("/api/review/<userid>/<albumid>")
def update_review(account_id, album_id):
    if not 'id' in session:
        return {"message": "not logged in"}, 400

    if is_banned():
        return {"message": "account banned from editing reviews"}, 403

    score, content = request.form['score'], request.form['content']

    cursor = sql.get_db().cursor()

    cursor.execute("SELECT * FROM Review WHERE AccountID = %s AND AlbumID = %s", (account_id, album_id))
    res = cursor.fetchone()
    if res == None:
        return {"message": "no review found by user with id %s for album with id %s" %(account_id, album_id)}, 404
    
    if session['id'] == res[0] or is_admin():
        cursor.execute("UPDATE Review SET Score=%s, Content=%s WHERE ID = %s;", (score, content, session['id']))
        sql.get_db().commit()
        cursor.close()
        return jsonify(review_data(account_id, album_id)), 200

    # finish when bethany finishes review page

@reviews.delete("/api/review/<userid>/<albumid>")
def delete_review(account_id, album_id):
    if session['id'] != account_id and not is_admin():
        return {"message": "insufficient permissions"}, 401 # = Unauthorized
    
    cursor = sql.get_db().cursor()
    cursor.execute("DELETE FROM Review WHERE AccountID = %s AND AlbumID = %s;", (account_id, album_id))
    sql.get_db().commit()
    if cursor.rowcount > 0:
        cursor.close()
        return {"message": "review by user with id %s for album with id %s deleted" %(account_id, album_id)}, 200 # = OK
    else:
        cursor.close()
        return {"message": "no review found by user with id %s for album with id %s" %(account_id, album_id)}, 404 # = Not Found

@reviews.post("/api/review/<userid>/<albumid>/tags")
def update_review_tags(userid, albumid):
    if not 'id' in session:
        return {"message": "not logged in"}, 400 # = Bad Request
    
    tags, review_account_id, review_album_id = request.form['tags'], request.form['review_account_id'], request.form['review_album_id']
    cursor = sql.get_db().cursor()
    cursor.execute("UPDATE Tags SET Tags = %s WHERE AccountID = %s AND ReviewAccountID = %s AND ReviewAlbumID = %s;", (tags, session['id'], review_account_id, review_album_id))
    if (cursor.rowcount == 0):
        cursor.close()
        return {"message": "something went wrong"}, 500 # = Internal Server Error
    cursor.close()
    return {"message": "tags updated"}, 200 # = OK