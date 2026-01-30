from flask import Blueprint, render_template

bp = Blueprint("blog", __name__, url_prefix="/blog")

@bp.route("/")
def home():
    return render_template("home.html")