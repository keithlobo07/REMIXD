from flask import *
from app import sql, ph

utils = Blueprint('utils', __name__)

@utils.post("/api/authenticate")
def authenticate():
    email = request.form['email']
    given_password = request.form['password']

    cursor = sql.get_db().cursor()
    cursor.execute("SELECT ID, Password FROM Account WHERE email = %s", (email))
    results = cursor.fetchone()
    
    if results != None:
        ID, password = results
        try:
            # throws an exception if the hash doesnt match
            ph.verify(password, given_password)
            session['id'] = ID

            # good practice to rehash passwords where necessary
            if (ph.check_needs_rehash(password)):
                cursor.execute("UPDATE Account SET Password = %s WHERE ID = %s;" %(ph.hash(given_password)), ID)
                sql.get_db().commit()
            cursor.close()

            return redirect(url_for("pages.home")), 303 # = See Other (redirect w/ get)
        except:
            # password didnt match
            cursor.close()
            return redirect(url_for("pages.login_page")), 403 # = Forbidden
    else: # email didnt match
        cursor.close()
        return redirect(url_for("pages.login_page")), 403 # = Forbidden


@utils.route("/api/logout")
def logout():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for("pages.lander")), 303 # = See Other (redirect w/ get)


@utils.route("/api/session")
def session_check():
    # use this to check if you are logged in
    [print(x, session[x]) for x in session]

    if 'id' in session:
        return {"message": "logged in as %d" %session['id']}, 200 # = OK
    return {"message": "not logged in"}, 200 # = OK