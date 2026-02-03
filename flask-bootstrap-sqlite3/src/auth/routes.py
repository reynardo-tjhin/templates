from flask import Blueprint, render_template, session, redirect, url_for

# create a blueprint (like a factory method)
# registered in __init__.py
bp = Blueprint('auth_routes', __name__, url_prefix="/auth")

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('blog.home'))