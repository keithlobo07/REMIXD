from flask import *
from app import sql, ph
from admin import is_admin

users = Blueprint('users', __name__)

def is_banned():
    if not 'id' in session:
        return False
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT modTags FROM Account WHERE ID = %s;" %(session['id']))
    result = cursor.fetchone()[0]
    cursor.close()
    return bool(result & 1)

def user_data(userid):
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT * FROM Account WHERE ID=%s LIMIT 1;",  str(userid))
    user = cursor.fetchone()
    if 'id' in session:
        # user is logged in -> perspective data
        cursor.execute("SELECT Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes, IFNULL(Tags.info & 128 = 128, 0) as user_like, IFNULL(Tags.info & 64 = 64, 0) as user_report FROM Review JOIN Account ON Account.ID = Review.AccountID LEFT JOIN Tags ON Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.AccountID = %s WHERE Review.AccountID=%s ORDER BY Review.timestamp DESC LIMIT 5;", (session['id'], userid))
        reviews = cursor.fetchall()
        cursor.close()
        
        return {
            "id":user[0],
            "name":user[1],
            "bio":user[5],
            "reviews":[{"albumid":x[0], "timestamp":x[1], "score":x[2], "liked":x[3], "content":x[4], "numLikes":x[5], "user_liked":x[6], "user_flagged":x[7]} for x in reviews]
        }
    else:
        # no login -> anonymous data
        cursor.execute("SELECT Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE Review.AccountID=%s ORDER BY Review.timestamp DESC LIMIT 5;", (userid))
        reviews = cursor.fetchall()
        cursor.close()
        
        return {
            "id":user[0],
            "name":user[1],
            "bio":user[5],
            "reviews":[{"albumid":x[0], "timestamp":x[1], "score":x[2], "liked":x[3], "content":x[4], "numLikes":x[5], "user_liked":x[6], "user_report":x[7]} for x in reviews]
        }

@users.get("/api/user/<userid>")
def user_lookup(userid):
    return jsonify(user_data(userid))

@users.post("/api/user")
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
                # some messed up database connection error would have to happen to get here but i'll account for it
                cursor.close()
                return {"message", "Error occured when retreiving new user from database."}, 500 # = Internal Server Error
            
            session['id'] = r[0]
            cursor.close()
            return redirect(url_for('pages.home')), 201 # = Created
        else:
            # user with this email already exists
            cursor.close()
            return {"message": "Email already exists."}, 409 # = Conflict
    else:
        return redirect(url_for('pages.home')), 303 # = See Other (redirect w/ get)

@users.put("/api/user/<userid>")
def update_user(userid):
    if session['id'] != userid and not is_admin():
        return {"message": "Insufficient permissions."}, 401 # = Unauthorized
    
    name, password, bio = request.form['name'], request.form['password'], request.form['bio']

    if name == None and password == None and bio == None:
        return {"message": "No data found in form."}, 400 # = Bad Request

    cursor = sql.get_db().cursor()

    cursor.execute("SELECT ID FROM Account WHERE ID = %s;", userid)
    if cursor.rowcount == 0:
        return {"message": "No user with ID %s found." %userid}, 404 # = Not Found

    message = ""

    # i could probably do this with string formatting but i wasnt sure how to do the commas between set statements
    if name != None:
        cursor.execute("UPDATE Account SET Name = %s WHERE ID = %s;", (name, userid))
        message += "Name updated. "
    if password != None:
        cursor.execute("UPDATE Account SET Password = %s WHERE ID = %s;", (password, userid))
        message += "Password updated. "
    if bio != None:
        cursor.execute("UPDATE Account SET Bio = %s WHERE ID = %s;", (bio, userid))
        message == "Bio updated. "
    
    sql.get_db().commit()
    cursor.close()

    return {"message": message}, 200

@users.delete("/api/user/<userid>")
def delete_user(userid):
    if session['id'] != userid and not is_admin():
        return {"message": "Insufficient permissions."}, 401 # = Unauthorized
    
    cursor = sql.get_db().cursor()
    cursor.execute("DELETE FROM Account WHERE ID = %s;", userid)
    if cursor.rowcount == 0:
        cursor.close()
        return {"message": "User with ID %s not found." %userid}, 404 # = Not Found
    
    if userid == session['id']:
        session.pop('id', None)

    cursor.close()
    return {"message": "User with ID %s deleted." %userid}, 200 # = OK