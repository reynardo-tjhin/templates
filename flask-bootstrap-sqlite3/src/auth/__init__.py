import functools

from flask import Blueprint, g, session, redirect, url_for
from src.db import get_db
from .api import bp as auth_api_bp
from .routes import bp as auth_routes_bp


# create a blueprint for the API, routes, etc.
bp = Blueprint("auth", __name__)

# register the blueprints
bp.register_blueprint(auth_api_bp)
bp.register_blueprint(auth_routes_bp)


# registers a function that runs before the view function, 
# no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    
    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?;", (user_id,)
        ).fetchone()


# This decorator returns a new view function that wraps 
# the original view it’s applied to. The new function checks 
# if a user is loaded and redirects to the login page otherwise. 
# If a user is loaded the original view is called and continues 
# normally.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth_routes.login"))
        
        return view(**kwargs)
    
    return wrapped_view