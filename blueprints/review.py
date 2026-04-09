from flask import *
from app import sql
from admin import is_admin
from user import is_banned

reviews = Blueprint('reviews', __name__)

def review_data(userid, albumid):
    cursor = sql.get_db().cursor()

    a = is_admin()

    if 'id' in session:
        cursor.execute("SELECT Review.AccountID, Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, IFNULL(Tags.info & 128 = 128, 0) as user_like, IFNULL(Tags.info & 64 = 64, 0) as user_report, (SELECT Account.Name From Account WHERE ID=Review.AccountID) as author FROM Review LEFT JOIN Tags ON Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.AccountID = %s WHERE Review.AccountID=%s AND AlbumID=%s;", (session['id'], userid, albumid))
        data = cursor.fetchone()
        cursor.close()

        if data == None:
            return None

        return {
            "accountID":data[0],
            "albumID":data[1],
            "name":data[9],
            "timestamp":data[2],
            "score":data[3],
            "liked":data[4],
            "content":data[5],
            "numLikes":data[6],
            "user_liked":data[7],
            "user_report":data[8],
            "is_admin":a
        }
    else:
        cursor.execute("SELECT AccountID, AlbumID, timestamp, Score, Liked, Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, (SELECT Account.Name From Account WHERE ID=Review.AccountID) as author FROM Review WHERE AccountID=%s AND AlbumID=%s;", (userid, albumid))
        data = cursor.fetchone()
        cursor.close()

        if data == None:
            return None

        return {
            "accountID":data[0],
            "albumID":data[1],
            "name":data[7],
            "timestamp":data[2],
            "score":data[3],
            "liked":data[4],
            "content":data[5],
            "numLikes":data[6],
            "is_admin":a
        }

@reviews.get("/api/review/<userid>/<albumid>")
def review_lookup(userid, albumid):
    data = review_data(userid, albumid)
    if data == None:
        return {"message": "No review from user with ID %s for album with ID %s found." %(userid, albumid)}, 404
    return data, 200

@reviews.post("/api/review")
def post_review():
    if not 'id' in session:
        return {"message": "Not logged in."}, 400
    
    if is_banned():
        return {"message": "Account banned from posting reviews."}, 403

    album_id, score, content = request.form['album_id'], request.form['score'], request.form['content']

    # finish when bethany finishes review page

@reviews.put("/api/review/<userid>/<albumid>")
def update_review(account_id, album_id):
    if not 'id' in session:
        return {"message": "Not logged in."}, 400

    if is_banned():
        return {"message": "Account banned from editing reviews."}, 403

    score, content = request.form['score'], request.form['content']

    cursor = sql.get_db().cursor()

    cursor.execute("SELECT * FROM Review WHERE AccountID = %s AND AlbumID = %s", (account_id, album_id))
    res = cursor.fetchone()
    if res == None:
        return {"message": "No review found by user with ID %s for album with ID %s." %(account_id, album_id)}, 404
    
    if session['id'] == res[0] or is_admin():
        cursor.execute("UPDATE Review SET Score=%s, Content=%s WHERE ID = %s;", (score, content, session['id']))
        sql.get_db().commit()
        cursor.close()
        return jsonify(review_data(account_id, album_id)), 200

    # finish when bethany finishes review page

@reviews.delete("/api/review/<userid>/<albumid>")
def delete_review(account_id, album_id):
    if session['id'] != account_id and not is_admin():
        return {"message": "Insufficient permissions."}, 401 # = Unauthorized
    
    cursor = sql.get_db().cursor()
    cursor.execute("DELETE FROM Review WHERE AccountID = %s AND AlbumID = %s;", (account_id, album_id))
    cursor.execute("DELETE FROM Tags WHERE ReviewAccountID = %s AND ReivewAlbumID = %s;", (account_id, album_id))
    sql.get_db().commit()
    if cursor.rowcount > 0:
        cursor.close()
        return {"message": "Review by user with ID %s for album with ID %s deleted." %(account_id, album_id)}, 200 # = OK
    else:
        cursor.close()
        return {"message": "No review found by user with ID %s for album with ID %s." %(account_id, album_id)}, 404 # = Not Found

@reviews.post("/api/review/<userid>/<albumid>/tags")
def update_review_tags(userid, albumid):
    if not 'id' in session:
        return {"message": "Not logged in"}, 400 # = Bad Request
    
    tags = request.form['tags']

    cursor = sql.get_db().cursor()
    cursor.execute("SELECT 1 FROM Tags WHERE AccountID = %s AND ReviewAccountID = %s AND ReviewAlbumID = %s;", (session['id'], userid, albumid))
    
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (%s, %s, %s, %s)", (session['id'], userid, albumid, tags))
    else:
        cursor.execute("UPDATE Tags SET info = %s WHERE AccountID = %s AND ReviewAccountID = %s AND ReviewAlbumID = %s;", (tags, session['id'], userid, albumid))
        
    sql.get_db().commit()
    cursor.close()
    return {"message": "Tags updated."}, 200 # = OK