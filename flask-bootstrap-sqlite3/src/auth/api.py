from flask import Blueprint, jsonify, request, session, Response, g
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash

from src.db import get_db

bp = Blueprint("auth_api", __name__, url_prefix="/api/v1/auth")

@bp.route("/register", methods=["POST"]) # type: ignore
def register() -> (Response | None):
    if (request.method == "POST"):
        
        # get user's username and password
        data = request.get_json()
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        
        # validation 1: username and password cannot be empty
        if not username:
            return jsonify({
                "status": "error",
                "message": "username cannot be empty",
            }), 400
        elif not password1:
            return jsonify({
                "status": "error",
                "message": "First Password cannot be empty",
            }), 400
        elif not password2:
            return jsonify({
                "status": "error",
                "message": "Second Password cannot be empty",
            }), 400
            
        # validation 2: password1 and password2 must match
        if (password1 != password2):
            return jsonify({
                "status": "error",
                "message": "First and Second Passwords are not the same",
            }), 400
            
        # validation 3: username should not exist in the database
        db = get_db()
        user = db.execute('SELECT username FROM user WHERE username = ?;', (username,)).fetchone()
        if user:
            return jsonify({
                "status": "error",
                "message": "username already exists",
            }), 400
            
        # insert into the database
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?);",
                (username, generate_password_hash(password1)),
            )
            db.commit()
            
            # insert successful, user still has to relogin
            # there may be a race condition on who will first insert/read where username = username
            # therefore, it's better to let the user to relogin
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error from execution of db: {e}",
            }), 404
            
        return jsonify({
            "status": "success",
            # "message": "user successfully added to database",
            "message": "please log in again",
        }), 201
        
@bp.route("/login", methods=["POST"]) # type: ignore
def login() -> (Response | None):
    if (request.method == "POST"):
        
        # get user's login details
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # validation 1: username and password cannot be empty
        if not username:
            return jsonify({
                "status": "error",
                "message": "username cannot be empty",
            }), 400
        elif not password:
            return jsonify({
                "status": "error",
                "message": "password cannot be emtpy",
            }), 400
            
        # validation 2: user must exist
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE username = ?;", (username,)).fetchone()
        if (user is None):
            return jsonify({
                "status": "error",
                "message": "user does not exist",
            }), 404
        
        # validation 3: password must match with the database
        if (not check_password_hash(user['password'], password)):
            return jsonify({
                "status": "error",
                "message": "password is incorrect",
            }), 400
            
        # perform the login operation
        # session is a dict that stores data across requests. When 
        # validation succeeds, the user’s id is stored in a new session. 
        # The data is stored in a cookie that is sent to the browser, 
        # and the browser then sends it back with subsequent requests. 
        # Flask securely signs the data so that it can’t be tampered with.
        session.clear()
        session['user_id'] = user['id']
        
        return jsonify({
            "status": "success",
            "message": "user successfully login",
        }), 200

@bp.route("/user", methods=["GET"]) # type: ignore
def user() -> (Response | None):
    if (request.method == "GET"):
        # get user id from session
        user_id = session.get("user_id")
        if (user_id is None):
            return jsonify({
                "status": "success",
                "message": "user has not logged in"
            }), 401
        
        # get id and username
        db = get_db()
        user = db.execute("SELECT id, username FROM user WHERE id = ?;", (user_id,)).fetchone()
        if (user is None):
            return jsonify({
                "status": "error",
                "message": f"could not find user with id '{user_id}'",
            }), 404
        
        return jsonify({
            "status": "success",
            "message": {
                "id": user['id'],
                "username": user['username'],
            }
        }), 200
        
@bp.route("/csrf-token", methods=["GET"])
def get_csrf_token():
    """
    Get a new CSRF token
    """
    # user is not signed in
    if (g.user is None):
        return jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401
        
    # generate CSRF token and store it in Flask's session
    # CSRF token is unique per session
    # generated per-session and stored in the session
    # not tied to a specific user account
    signed_csrf_token = generate_csrf() # returns the signed token
    # the same with g.csrf_token
    
    # get the CSRF token from session
    # session.get("csrf_token") stores the real token
    return jsonify({
        "status": "ok",
        "message": signed_csrf_token,
    })