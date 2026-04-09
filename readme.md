remixd
======
A letterboxd like social media for reviewing albums.

Dependancies:
-------------
+ flask
+ flask-mysql
+ pyopenssl
+ argon2-cffi

Hosting:
------
1. Install python dependancies
2. (optional) Host mysql locally if aws isnt working (we probably ran out of credits)
    1. Setup local mysql server
    2. Run sql_scripts/database_setup.sql
    3. (optional) Run sql_scripts/insert_data.sql for example data
    4. Edit lines 12 - 15 of app.py to reflect new connection
2. Run app.py
3. Access with provided host (e.g. https://127.0.0.1:5000)

**warning:** Your web browser will probably try to stop you from accessing any pages since the ssl certificate is self-certified. Most browsers include an override.

API Usage:
----------
<h3>Albums</h3>
<h4>Album information</h4>
Format: /api/album/\<albumid\> <br>
Example request: /api/album/21159e3f-172e-43f6-aa7d-8e06a81fea49<br>
Example response:<br><br>
Returns relevant information for a specific album given its Musicbrainz release group ID. Takes at least one second to execute since it needs to adhere to Musicbrainz's rate limits. Includes the tracklist of the release group's earliest release.

<h4>Album reviews</h4>
Format: /api/album/\<albumid\>/reviews<br>
Example request: /api/album/21159e3f-172e-43f6-aa7d-8e06a81fea49/reviews?limit=3
Example response: <br><br>
Returns a number (default 5) of reviews for an album given its Musicbrainz id.

<h4>Album search</h4>
Format: /api/albums?query="\<queryphrase\>"<br>
Example request: /api/albums?query="Illmatic"<br>
Example response: <br><br>
Searches the Musicbrainz database using their api and returns the release groups matching the given phrase. Includes artist and release group title.<br>
Returns 400 if query parameter is missing.

---

<h3>Users</h3>
<h4>Lookup / Get</h4>
Format: /api/user/\<userid\><br>
Required method: Get<br>
Example request: /api/user/1<br>
Example response: <br><br>
Returns impersonal information about a user. Includes their five most recent reviews. If you have an active login, the reviews will contain like and report data from your perspective.

<h4>Post</h4>
Format: /api/user<br>
Required method: Post<br>
Required body: form containing email, username and password fields<br>
Example request: <br>
Example response: <br>
HTTP response codes:<br>
- 201 on successful account creation<br>
- 303 to home page if already logged in<br>
- 409 where account with given email already exists<br>
- 500 if database cannot retrieve newly created user<br><br>

Creates a user account with the provided information. Automatically logs in as the new user.

<h4>Put</h4>
Format: /api/user/\<userid\><br>
Required method: Put<br>
Required body: form containing at least one of 'name', 'password', or 'bio'<br>
Example request:<br>
Example response:<br>
HTTP response codes:<br>
- 200 if user was updated<br>
- 400 if form contains none of 'name', 'password', or 'bio'<br>
- 401 if trying to edit another user<br><br>

Updates a user account with the provided information. Admins can change any user's information. Standard users can only change their own. Returns a message detailing what fields were changed.

<h4>Delete</h4>
Format: /api/user/\<userid\><br>
Required method: Delete<br>
Example request:<br>
Example response:<br>
HTTP response codes:<br>
- 200 on successful deletion<br>
- 401 if trying to delete another user<br>
- 404 if no user matching given ID is found<br><br>

Removes a user account from the database. Admins may delete any user. Standard users can only delete their own account. Logs user out if deleting themselves. Returns a message expanding upon HTTP codes.

---

<h3>Reviews</h3>
<h4>Lookup / Get</h4>
Format: /api/review/\<userid\>/\<albumid\><br>
Required method: Get
Example request: /api/review/1/21159e3f-172e-43f6-aa7d-8e06a81fea49<br>
Example response:<br>
HTTP response codes:<br>
- 404 if review could not be found<br>
- 200 on successful lookup<br><br>

Returns one specific review given a user and Musicbrainz release group id. If you have an active login, the review will contain like and report data from your perspective. If no review could be found, returns a message explaining so.

<h4>Post</h4>
Format: /api/review<br>

<h4>Put</h4>
Format:

<h4>Delete</h4>
Format: /api/review/\<userid\>/\<albumid\><br>
Required method: Delete<br>
Example request: <br>
Example response: <br>
HTTP response codes: <br>
- 200 on successful deletion<br>
- 404 if review could not be found<br>
- 401 if trying to delete someone else's review<br><br>

Deletes a review from the database. Admins may delete any review. Standard users can only delete their own. Deletes all records of likes and reports from the database as well.

<h4>Tags</h4>
Format: /api/review/\<userid\>/\<albumid\>/tags<br>
Required method: Post<br>
Example request: <br>
Example response: <br>
HTTP response codes: <br>
- 400 if not logged in<br>
- 200 on successful tag update<br><br>

Updates the tag information (likes, reports) on a given review from the currently logged in user. 

---

<h3>Admin</h3>
<h4>Review search</h4>
Format: /api/admin/reviews<br>
Example response:<br><br>
Returns the 5 most reported reviews.

<h4>User search</h4>
Format: /api/admin/users<br>
Example response:<br><br>
Returns 5 users with the highest total review reports.

<h4>Statistics</h4>
Format: /api/admin/statistics<br>
Example response:<br><br>
Returns the number of posts made each month for the past 12 months.

<h4>Ban user</h4>
Format: /api/admin/ban/\<userid\>
Example request: /api/admin/ban/1<br>
Example response: {"message":"User 1 banned."}, 200<br>
HTTP response codes:<br>
- 200 on successful ban<br>
- 404 if no user with given id found<br><br>

Disables a user's ability to post and edit reviews. Deletes all current reviews and tags on posts. Account stays within database so email cannot be reused.

---

<h3>Utilities</h3>

<h4>Log in / Authenticate</h4>
Format: /api/authenticate **POST method only**<br>
Required body: form containing email and username<br>
Example request: <br>
Example response: <br>
HTTP response codes:<br>
- 303 to home page on successful login <br>
- 403 on incorrect login <br><br>

Logs in as the user associated with the given email and password. Adds user id to Flask's built-in session data. Redirects to the home page on successful log in.

<h4>Log out</h4>
Format: /api/logout<br>
Example response: <br>
HTTP response codes: <br>
- 303 to lander page <br><br>

Logs out the current user if any. Removes the current id from Flask's built-in session data. Redirects to the lander page.

<h4>Session</h4>
Format: /api/session<br>
Returns a message with information about what user is currently logged in if any.