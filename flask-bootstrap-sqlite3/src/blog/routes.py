from flask import Blueprint, render_template

bp = Blueprint("blog_routes", __name__, url_prefix="/blog")

@bp.route("/")
def home():
    return render_template("blog/home.html")