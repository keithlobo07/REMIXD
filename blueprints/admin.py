from flask import *
from app import sql

admins = Blueprint('admins', __name__)


def is_admin():
    if not 'id' in session:
        return False
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT isAdmin FROM Account WHERE ID = %s;", session['id'])
    result = cursor.fetchone()
    return result[0]

@admins.route("/api/admin/reviews")
def admin_review_search():
    if (not is_admin()):
        return {"message": "insufficient permissions"}, 409 # = Forbidden
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT *, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 64) AS Reports, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review ORDER BY Reports DESC LIMIT 5;")
    results = cursor.fetchall()
    cursor.close()

    return jsonify({
        "reviews":[{"accountID":x[0], "albumID":x[1], "timestamp":x[2], "score":x[3], "liked":x[4], "content":x[5], "reports":x[6], "likes":x[7]} for x in results]
    })

@admins.route("/api/admin/users")
def admin_user_search():
    if (not is_admin()):
        return {"message": "insufficient permissions"}, 409 # = Forbidden
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT ReviewAccountID, (SELECT Name FROM Account WHERE ID = Tags.ReviewAccountID) AS Name, COUNT(*) AS `Total Reports` FROM Tags WHERE info & 64 GROUP BY ReviewAccountID ORDER BY `Total Reports` LIMIT 5;")
    results = cursor.fetchall()
    cursor.close()

    return jsonify({
        "users":[{"accountID":x[0], "name":x[1], "numReports":x[2]} for x in results]
    })

@admins.route("/api/admin/statistics")
def admin_stats():
    if (not is_admin()):
        return {"message": "insufficient permissions"}, 409 # = Forbidden
    cursor = sql.get_db().cursor()
    # yes this query is a nightmare but it works in one query and thats better than it being good and not working
    cursor.execute("SELECT (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 0 MONTH)),(SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 1 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 13 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 2 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 3 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 4 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 5 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 6 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 8 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 7 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 9 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 8 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 10 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 9 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 11 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 10 MONTH)), (SELECT COUNT(*) FROM Review WHERE timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 12 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 DAY), INTERVAL 11 MONTH));")
    results = cursor.fetchone()
    cursor.close()

    return jsonify({
        "data":results
    })

@admins.route("/api/admin/ban/<userid>")
def ban_user(userid):
    if (not is_admin()):
        return {"message": "insufficient permissions"}, 409 # = Forbidden
    
    cursor = sql.get_db().cursor()
    cursor.execute("UPDATE Account SET modFlags = 1 WHERE ID = %s;", userid)
    sql.get_db().commit()

    if (cursor.rowcount == 0):
        return {"message": "no user with id %s found" %userid}, 404 # = Not Found
    else:
        
        return {"message":"user %s banned" %userid}, 200 # = Completes