from flask import Blueprint, jsonify

bp = Blueprint("blog_api", __name__, url_prefix="/api/v1/blog")

@bp.route("/", methods=["GET"])
def posts():
    """
    Returns all the posts
    """
    return jsonify({
        "status": "ok",
        "message": "blog API init",
    })

@bp.route("/post/<int:id>", methods=["GET"]) # type: ignore
def read_post(id: int):
    """
    Get a specific post based on id
    """

@bp.route("/post", methods=["POST"]) # type: ignore
def create_post():
    """
    Create a new post
    """

@bp.route("/post/<int:id>", methods=["PUT"]) # type: ignore
def update_post(id: int):
    """
    Update an existing post
    """

@bp.route("/post/<int:id>", methods=["DELETE"]) # type: ignore
def delete_post(id: int):
    """
    Delete an existing post
    """