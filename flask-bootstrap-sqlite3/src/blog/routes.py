from flask import Blueprint, render_template
from src.auth import login_required

bp = Blueprint("blog_routes", __name__, url_prefix="/blog")

@bp.route("/")
def home():
    return render_template("blog/home.html")

@bp.route("/create")
def create():
    return render_template("blog/create.html", title="Create a New Post!")

@bp.route("/update/<int:post_id>")
@login_required
def update(post_id: int):
    """
    Create this view to pass the post_id to get the post details
    """
    return render_template("blog/create.html", title="Edit post")