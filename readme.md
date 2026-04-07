remixd
======
A letterboxd like social media for reviewing albums.

dependancies:
-------------
+ flask
+ flask-mysql
+ pyopenssl
+ argon2-cffi

hosting:
------
1. install python dependancies
2. (optional) host mysql locally if aws isnt working
    1. setup local mysql server
    2. run sql_scripts/database_setup.sql
    3. (optional) run sql_scripts/insert_data.sql for example data
    4. edit lines 12 - 15 of app.py to reflect new connection
2. run app.py
3. access with provided host (e.g. https://127.0.0.1:5000)

**warning:** your web browser will probably try to stop you from accessing any pages since the ssl certificate is self-certified. most browsers include an override.

api usage:
----------
<h3>lookup</h3>

<h4>album</h4>
<p>format: **figure out escaping characters** <br>
example request: /api/album/21159e3f-172e-43f6-aa7d-8e06a81fea49<br>
example response:<br><br>
returns relevant information for a specific album given its musicbrainz release group id. takes at least one second to execute since it needs to adhere to musicbrainz's rate limits. includes the tracklist of the release group's earliest release.
</p>

<h4>user</h4>
<p>format: <br>
example request: /api/user/1<br>
example response: <br><br>
returns impersonal information about a user. returns their five most recent reviews. if you have an active login, the reviews will contain like and report data from your perspective.</p>

<h4>review</h4>
<p>format: <br>
example request: /api/review/1/21159e3f-172e-43f6-aa7d-8e06a81fea49<br>
example response:<br><br>
returns one specific review given a user and musicbrainz release group id. if you have an active login, the review will contain like and report data from your perspective.
</p>

---

<h3>search</h3>

<h4>album search</h4>
<p>format: /api/albums?query=""<br>
example request: /api/albums?query="Illmatic"<br>
example response: <br><br>
searches the musicbrainz database using their api and returns the release groups matching the given phrase. includes artist and release group title.<br>
returns 400 if query parameter is missing.
</p>

<h4>album recommend</h4>

---

<h3>admin</h3>

<h4>review search</h4>
<p>format: /api/admin/reviews<br>
example response:<br><br>
returns the 5 most reported reviews.
</p>

<h4>user search</h4>
<p>format: /api/admin/users<br>
example response:<br><br>
returns 5 users with the highest total review reports.
</p>

<h4>statistics</h4>

---

<h3>utilities</h3>
<h4>sign up</h4>
format: /api/signup **PUT method only**<br>
required body: form containing email, username and password fields<br>
example request: <br>
example response: <br>
http response codes:<br>
- 201 on successful account creation<br>
- 303 to home page if already logged in<br>
- 409 where account with given email already exists<br>
- 500 if database cannot retrieve newly created user<br><br>

creates a user account with the provided information. automatically logs in as the new user.


<h4>log in / authenticate</h4>
format: /api/authenticate **POST method only**<br>
required body: form containing email and username<br>
example request: <br>
example response: <br>
http response codes:<br>
- 303 to home page on successful login <br>
- 403 on incorrect login <br><br>

logs in as the user associated with the given email and password. adds user id to Flask's built-in session data. redirects to the home page on successful log in.

<h4>log out</h4>
format: /api/logout<br>
example response: <br>
http response codes: <br>
- 303 to lander page <br><br>

logs out the current user if any. removes the current id from Flask's built-in session data. redirects to the lander page.

<h4>session</h4>
<p>format: /api/session<br>
returns a message with information about what user is currently logged in if any.
</p>