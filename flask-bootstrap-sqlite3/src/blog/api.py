from flask import Blueprint, jsonify, request, g
from src.db import get_db

bp = Blueprint("blog_api", __name__, url_prefix="/api/v1/blog")

@bp.route("/posts", methods=["GET"])
def posts():
    """
    Returns all the posts
    """
    # get all the posts from database
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC;"
    ).fetchall()
    
    # convert into a JSON-parsable object
    posts = [
        {**dict(post)}
        for post in posts
    ]
    return jsonify({
        "status": "ok",
        "message": posts,
    }), 200

@bp.route("/posts/<int:post_id>", methods=["GET"]) # type: ignore
def get_post(post_id: int):
    """
    Get a specific post based on the id
    """
    db = get_db()
    post = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?;", (post_id,)
    ).fetchone()
    
    # validation 1: post not found -> return 404
    if (post is None):
        return jsonify({
            "status": "error",
            "message": f"invalid post_id '{post_id}'",
        }), 404
    
    # convert into a JSON-parsable object
    post = {**dict(post)}
    
    return jsonify({
        "status": "ok",
        "message": post,
    }), 200

@bp.route("/posts", methods=["POST"]) # type: ignore
def create_post():
    """
    Create a new post
    """
    if (request.method == "POST"):
        # get the data
        data = request.get_json()
        title = data.get('title')
        body = data.get('body')
        
        # validation 1: title and body should not be null (missing title/body)
        if (title is None):
            return jsonify({
                "status": "error",
                "message": "title cannot be empty",
            }), 400
        
        if (body is None):
            return jsonify({
                "status": "error",
                "message": "body cannot be empty",
            }), 400
        
        # validation 2: ensuring that g.user is not None (user is logged in)
        if (g.user is None):
            return jsonify({
                "status": "error",
                "message": "author unknown",
            }), 401
        
        # add the new post
        db = get_db()
        db.execute(
            "INSERT INTO post (title, body, author_id)"
            " VALUES (?, ?, ?);",
            (title, body, g.user['id'])
        )
        db.commit()
        return jsonify({
            "status": "ok",
            "message": "successfully added a new post",
        }), 201
        

@bp.route("/posts/<int:post_id>", methods=["PUT"]) # type: ignore
def update_post(post_id: int):
    """
    Update an existing post
    """
    if (request.method == "PUT"):
        data = request.get_json()
        title = data.get('title')
        body = data.get('body')
        
        # validation 1: check that the post exists
        db = get_db()
        post = db.execute("SELECT id, author_id FROM post WHERE id = ?;", (post_id,)).fetchone()
        if (post is None):
            return jsonify({
                "status": "error",
                "message": "post does not exist",
            }), 404
        
        # validation 2: title should not be empty
        if (title is None):
            return jsonify({
                "status": "error",
                "message": "title cannot be empty",
            }), 400
        
        # validation 3: only the user can edit
        if (post['author_id'] != g.user['id']):
            return jsonify({
                "status": "error",
                "message": "unauthorised",
            }), 403
        
        # update the entire post
        db.execute(
            "UPDATE post SET title = ?, body = ?"
            " WHERE id = ?;", (title, body, post_id)
        )
        db.commit()
        return jsonify({
            "status": "success",
            "message": "successfully updated the post with a new title and body",
        }), 200
        
@bp.route("/posts/<int:post_id>", methods=["PATCH"]) # type: ignore
def patch_post(post_id: int):
    """
    Patch an existing post (partial update)
    """
    if (request.method == "PATCH"):
        data = request.get_json()
        
        # validation 1: check if post exists
        db = get_db()
        post = db.execute("SELECT id, author_id FROM post WHERE id = ?;", (post_id)).fetchone()
        if (post is None):
            return jsonify({
                "status": "error",
                "message": "post does not exist",
            }), 404
            
        # validation 2: author id and the current user match
        if (post['author_id'] != g.user['id']):
            return jsonify({
                "status": "error",
                "message": "unauthorized",
            }), 403
        
        # update title
        if ('title' in data):
            db.execute("UPDATE post SET title = ?;", (data['title'],))
            db.commit()
    
        # update body
        if ('body' in data):
            db.execute("UPDATE post SET body = ?;", (data['body'],))
            db.commit()
        
        return jsonify({
            "status": "success",
            "message": "successfully updated post",
        }), 200
    

@bp.route("/posts/<int:post_id>", methods=["DELETE"]) # type: ignore
def delete_post(post_id: int):
    """
    Delete an existing post
    """
    if (request.method == "DELETE"):
        
        # validation 1: post exists
        db = get_db()
        post = db.execute("SELECT id, author_id FROM post WHERE id = ?;", (post_id,)).fetchone()
        if (post is None):
            return jsonify({
                "status": "error",
                "message": "post does not exist",
            }), 404
        
        # validation 2: user is the same as the creator of the post
        if (g.user['id'] != post['author_id']):
            return jsonify({
                "status": "error",
                "message": "unauthorized",
            }), 403
            
        db.execute("DELETE FROM post WHERE id = ?;", (post_id,))
        db.commit()
        return jsonify({
            "status": "success",
            "message": "post successfully deleted",
        }), 200