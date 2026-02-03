from flask import Blueprint

from .api import bp as blog_api_bp


# create a blueprint for the API, routes, etc.
bp = Blueprint("blog", __name__)

# register the blueprints
bp.register_blueprint(blog_api_bp)