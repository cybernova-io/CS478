from os import abort
from flask import (
    Blueprint,
    request,
    jsonify,
)
from flask_jwt_extended import jwt_required, current_user
from ..models.Posts import Post, PostLike, PostComment, db
from flask_login import logout_user
from flask import current_app as app
from sqlalchemy import engine, create_engine
from ..services.WebHelpers import WebHelpers


post_bp = Blueprint("post_bp", __name__)


@post_bp.route("/api/post", methods=["GET"])
@jwt_required()
def get_post():
    """
    GET: Get all posts

    """
    data = {}

    posts = Post.query.all()

    return jsonify([x.serialize() for x in posts])


# get specific post
@post_bp.route("/api/post/<int:id>", methods=["GET"])
@jwt_required()
def get_singlePost(id):
    """
    GET: return specific post of individual user
    """
    data = {}

    post = Post.query.get(id)

    if Post is None:
        return WebHelpers.EasyResponse("No post found with that id.", 404)

    else:
        return post.serialize()


# create post
@post_bp.route("/api/post/create/", methods=["POST"])
@jwt_required()
def create_post():
    title = request.form["title"]
    content = request.form["content"]

    post = Post(
        title=title,
        content=content,
    )

    db.session.add(post)
    db.session.commit()

    return WebHelpers.EasyResponse(f"{post.title} created.", 200)


# delete post
@post_bp.route("/api/post/delete/", methods=["DELETE"])
@jwt_required()
def delete_post():
    """
    Deletes Post
    """
    id = request.form["id"]
    post = Post.query.get(id)
    if post is None:
        """
        abort(404) returns an error
        i think crafting a data response with a 404 error code returned will work
        """
        abort(404)

    db.session.delete(post)
    db.session.commit()
    data = {"status": 200, "msg": str(post.title) + " deleted."}

    return data


# update posts
@post_bp.route("/api/post/update/", methods=["PUT"])
@jwt_required()
def update_post():
    """
    Updates Post
    """
    id = request.form["id"]
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get(id)

    post.title = title
    post.content = content

    db.session.commit()

    data = {
        "status": 200,
        "content": post.content,
        "msg": str(post.title) + " updated.",
    }
    return data


@post_bp.route("/api/post/like/<int:post_id>/", methods=["POST"])
@jwt_required()
def user_likes_post(post_id):
    """
    Like a post
    """

    post = Post.query.filter_by(id=post_id).first_or_404()

    if post is None:
        return WebHelpers.EasyResponse("Specified post does not exist.", 404)
    post_like = (
        PostLike.query.filter(PostLike.user_id == current_user.id)
        .filter(PostLike.post_id == post.id)
        .first()
    )
    if post_like is None:

        post_like = PostLike(user_id=current_user.id, post_id=post_id)

        db.session.add(post_like)
        db.session.commit()
        return WebHelpers.EasyResponse("success", 200)
    else:
        return WebHelpers.EasyResponse("You have already liked this post.", 400)


@post_bp.route("/api/post/unlike/<int:post_id>/", methods=["POST"])
@jwt_required()
def user_unlike_post(post_id):
    """
    unlike a post
    """
    post = Post.query.filter_by(id=post_id).first_or_404()

    if post is None:
        return WebHelpers.EasyResponse("Specified post does not exist.", 404)
    else:
        post_like = (
            PostLike.query.filter(PostLike.user_id == current_user.id)
            .filter(PostLike.post_id == post.id)
            .first()
        )
        db.session.delete(post_like)
        db.session.commit()
        return WebHelpers.EasyResponse("success", 200)


@post_bp.route("/api/post/comment/<int:post_id>/", methods=["POST"])
@jwt_required()
def user_comment_post(post_id):
    """
    comment on a post
    """
    post = Post.query.filter_by(id=post_id).first_or_404()

    if post is None:
        return WebHelpers.EasyResponse("Specified post does not exist.", 404)
    # post_comment = PostComment.query.filter(PostComment.user_id==current_user.id).filter(PostComment.post_id==post.id).first()
    text = request.form["text"]
    post_comment = PostComment(user_id=current_user.id, post_id=post.id, text=text)
    db.session.add(post_comment)
    db.session.commit()
    return WebHelpers.EasyResponse("success", 200)
