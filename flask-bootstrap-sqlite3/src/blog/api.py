from flask import Blueprint, jsonify

bp = Blueprint("blog_api", __name__, url_prefix="/api/v1/blog")

@bp.route("/", methods=["GET"])
def posts():
    return jsonify({
        "status": "ok",
        "message": "blog API init",
    })