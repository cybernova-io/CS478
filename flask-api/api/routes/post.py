from os import abort
from flask import (
    Blueprint,
    request,
    jsonify,
    Response,
    render_template,
    flash,
    redirect
)
from flask_jwt_extended import jwt_required, current_user
from ..models.Posts import Post, PostLike, PostComment, db
from flask_login import logout_user
from flask import current_app as app
from sqlalchemy import engine, create_engine
from ..services.WebHelpers import WebHelpers
from api.models.Users import Group, User

post_bp = Blueprint("post_bp", __name__)


# get specific post
@post_bp.route("/post/<int:id>", methods=["GET"])
@jwt_required()
def get_singlepost_page(id : int):
    """
    GET: return specific post of individual user
    """
    data = {}
    post = Post.query.get(id)

    data = post.serialize()

    for x in data['comments']:
        user : User
        user = User.query.get(x['userId'])
        x['name'] = f'{user.first_name} {user.last_name}'

    post_user = User.query.get(data['userId'])

    data["user"] = post_user.serialize()    

    if post:
        return render_template('/posts/single-post.html', post=data)
    return flash('Sorry, that post could not be found!')

@post_bp.route("/post/comment/<int:post_id>", methods=["POST"])
@jwt_required()
def user_comment_post_page(post_id):
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
    return redirect(f'/post/{post_id}')

    

######################################################### API BELOW, SERVER RENDERING ABOVE
@post_bp.route("/api/posts/", methods=["GET"])
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

#get all posts from a group
@post_bp.get("/api/group/<int:id>/post")
@jwt_required()
def get_group_posts(id : int) -> Response:
    
    group = Group.query.get(id)
    if group:
        resp = jsonify([x.serialize() for x in group.posts])
        resp.status_code = 200
        return resp


# create post
@post_bp.post("/api/posts/")
@jwt_required()
def create_post():

    title = request.form["title"]
    content = request.form["content"]

    post = Post(
        title=title,
        content=content,
        user_id = current_user.id
    )

    db.session.add(post)
    db.session.commit()

    return WebHelpers.EasyResponse(f"{post.title} created.", 200)

#create group post
@post_bp.post("/api/group/<int:id>/post")
@jwt_required()
def create_group_post(id : int) -> Response:

    group = Group.query.get(id)
    if group:
        if group.check_role(current_user) is not None:

            title = request.form['title']
            content = request.form['content']

            post = Post(
                title=title,
                content=content,
                user_id=current_user.id,
                group_id=group.id
            )
            db.session.add(post)
            db.session.commit()
            return WebHelpers.EasyResponse(f'Post added to group id ({id})', 200)
        return WebHelpers.EasyResponse(f'You must be in this group to make a post in it!', 400)
    return WebHelpers.EasyResponse(f'The specified group does not exist.', 400)

    


# delete post
@post_bp.route("/api/posts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_post(id):
    """
    Deletes Post
    """
    
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

#delete group post
@post_bp.delete("/api/group/<int:id>/post/<int:postId>")
@jwt_required()
def delete_group_post(id : int, postId : int) -> Response:

    group = Group.query.get(id)

    if group:
        post = Post.query.get(postId)
        if post:
            if group.check_role(current_user) == 'Owner' or group.check_role(current_user) == 'Moderator' or current_user.id == post.user_id:
                db.session.delete(post)
                db.session.commit()
                return WebHelpers.EasyResponse(f'Post id ({postId}) deleted from group id ({id})', 200)
            return WebHelpers.EasyResponse(f'You must be the post creator or group moderator to delete this post.', 400)
        return WebHelpers.EasyResponse(f'No post with id {postId} found.', 400)
    return WebHelpers.EasyResponse(f'No group with id ({id}) found.', 400)

# update posts
@post_bp.route("/api/posts/<int:id>", methods=["PUT"])
@jwt_required()
def update_post(id):
    """
    Updates Post
    """
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

#update group post
@post_bp.put("/api/group/<int:id>/post/<int:postId>")
@jwt_required()
def update_group_post(id : int, postId : int) -> Response:
    group = Group.query.get(id)

    if group:
        post = Post.query.get(postId)
        if post:
            if group.check_role(current_user) == 'Owner' or group.check_role(current_user) == 'Moderator' or current_user.id == post.user_id:

                title = request.form["title"]
                content = request.form["content"]
                post.title = title
                post.content = content
                db.session.commit()

                return WebHelpers.EasyResponse(f'Post id ({postId}) updated in group id ({id})', 200)
            return WebHelpers.EasyResponse(f'You must be the post creator or a group moderator to update this post.', 400)
        return WebHelpers.EasyResponse(f'No post with id {postId} found.', 400)
    return WebHelpers.EasyResponse(f'No group with id ({id}) found.', 400)

@post_bp.route("/api/posts/<int:post_id>/likes", methods=["POST"])
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

@post_bp.post("/api/group/<int:id>/post/<int:postId>/like")
@jwt_required()
def user_likes_group_post(id : int, postId : int) -> Response:
    group = Group.query.get(id)

    if group:
        post = Post.query.get(postId)
        if post:
            if group.check_role(current_user) != None:
                
                group_post_like = PostLike.query.filter(PostLike.user_id == current_user.id).filter(PostLike.group_id == group.id).filter(PostLike.post_id == post.id).first()
                if group_post_like is None:
                    group_post_like = PostLike(user_id=current_user.id, post_id=post.id, group_id=group.id)
                    db.session.add(group_post_like)
                    db.session.commit()
                    return WebHelpers.EasyResponse(f'User id ({current_user.id}) liked post ({postId}) in group id ({id}).', 200)
                return WebHelpers.EasyResponse(f'You have already liked this post.', 400)
            return WebHelpers.EasyResponse(f'You must be in this group to like posts.', 400)
        return WebHelpers.EasyResponse(f'No post with id {postId} found.', 400)
    return WebHelpers.EasyResponse(f'No group with id ({id}) found.', 400)

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

@post_bp.delete("/api/group/<int:id>/post/<int:postId>/unlike")
@jwt_required()
def user_unlikes_group_post(id : int, postId : int) -> Response:
    group = Group.query.get(id)

    if group:
        post = Post.query.get(postId)
        if post:
            if group.check_role(current_user) != None:
                
                group_post_like = PostLike.query.filter(PostLike.user_id == current_user.id).filter(PostLike.group_id == group.id).filter(PostLike.post_id == post.id).first()
                if group_post_like is not None:
                    db.session.delete(group_post_like)
                    db.session.commit()

                    return WebHelpers.EasyResponse(f'User id ({current_user.id}) unliked post ({postId}) in group id ({id}).', 200)
                return WebHelpers.EasyResponse(f'You have not liked this post.', 400)
            return WebHelpers.EasyResponse(f'You must be in this group to like posts.', 400)
        return WebHelpers.EasyResponse(f'No post with id {postId} found.', 400)
    return WebHelpers.EasyResponse(f'No group with id ({id}) found.', 400)


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

# when comments are retrieved it grabs any replies that have been made as well
@post_bp.route("/api/post/comment_response/<int:id>/", methods=["POST"])
@jwt_required()
def user_comment_response(id):
    comment = PostComment.query.filter_by(id=id).first_or_404()

    if comment is None:
        return WebHelpers.EasyResponse("Specified comment does not exist.", 404)
    text = request.form["text"]
    comment_response = PostComment(user_id=current_user.id, text=text, parent_id=comment.id)
    db.session.add(comment_response)
    db.session.commit()
    return WebHelpers.EasyResponse("success", 200)

@post_bp.route("/api/post/comment_like_response/<int:id>/", methods=["POST"])
@jwt_required()
def user_like_comment_response(id):
    comment = PostComment.query.filter_by(id=id).first_or_404()

    if comment is None:
        return WebHelpers.EasyResponse("Specified comment does not exist.", 404)
    comment_like = (
        PostComment.query.filter(PostComment.user_id == current_user.id)
        .filter(PostComment.id == id)
        .first()
    )
    if comment_like is None:

        comment_like = PostComment(user_id=current_user.id, id=PostComment.id)

        db.session.add(comment_like)
        db.session.commit()
        return WebHelpers.EasyResponse("success", 200)
    else:
        return WebHelpers.EasyResponse("You have already liked this comment.", 400)

@post_bp.post("/api/group/<int:id>/post/<int:postId>/comment")
@jwt_required()
def user_comments_group_post(id : int, postId : int) -> Response:
    group = Group.query.get(id)

    if group:
        post = Post.query.get(postId)
        if post:
            if group.check_role(current_user) != None:
                
                text = request.form['text']
                group_post_comment = PostComment(
                    user_id=current_user.id,
                    post_id=post.id,
                    group_id=group.id,
                    text=text
                )
                db.session.add(group_post_comment)
                db.session.commit()
    
                return WebHelpers.EasyResponse(f'User ({current_user.id}) left a comment on post id ({postId}) in group id ({id}).', 200)
            return WebHelpers.EasyResponse(f'You must be in this group to like posts.', 400)
        return WebHelpers.EasyResponse(f'No post with id {postId} found.', 400)
    return WebHelpers.EasyResponse(f'No group with id ({id}) found.', 400)

@post_bp.delete("/api/group/<int:id>/post/<int:postId>/comment/<int:commentId>")
@jwt_required()
def user_delete_comment_group_post(id : int, postId : int, commentId : int) -> Response:
    group = Group.query.get(id)

    if group:
        post = Post.query.get(postId)
        if post:
            if group.check_role(current_user) != None:
                
                comment = PostComment.query.filter(PostComment.id == commentId).filter(PostComment.user_id == current_user.id).first()
                if comment:
                    if current_user.id == comment.id or group.check_role(current_user) == 'Owner' or group.check_role(current_user) == 'Moderator' \
                    or 'Admin' in current_user.roles:
                        db.session.delete(comment)
                        db.session.commit()
                        return WebHelpers.EasyResponse(f'Comment deleted.', 200)
                    return WebHelpers.EasyResponse(f'You must be the comment creater or have elevated privileges to delete this comment.', 400)
                return WebHelpers.EasyResponse(f'Comment not found.', 400)
            return WebHelpers.EasyResponse(f'You must be in this group to like posts.', 400)
        return WebHelpers.EasyResponse(f'No post with id {postId} found.', 400)
    return WebHelpers.EasyResponse(f'No group with id ({id}) found.', 400)