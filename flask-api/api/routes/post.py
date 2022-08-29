from os import abort
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from ..models import Likes, db, Post
from .. import login_manager
from flask_login import logout_user
import werkzeug

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/api/post/', methods=['GET'])
@login_required
def get_post():
    """
    GET: Get all posts
    
    """
    data = {}

    posts = Post.query.all()
    for i in posts:
        data[i.id] = {
            'status': 200,
            'title': i.title,
            'content': i.content
        }

    return data


@post_bp.route('/api/post/<int:id>', methods=['GET'])
def get_singlePost(id):
    """
    GET: return specific post of individual user 
    """
    data = {}

    post = Post.query.get(id)

    if Post is None:

        data = {
            'status': 404,
            'msg': 'No post found with that id.'
        }
        return data

    else:
        data = {
            'status': 200,
            'title': post.title,
            'content': post.content,
            'msg': str(post.title) + ' Retrieved.' 
        }

    return data

#create post
@post_bp.route('/api/post/create/', methods=['POST'])
@login_required
def create_post():
    title = request.form['title']
    content = request.form['content']

    post = Post(
        title = title,
        content = content,
        owner = current_user.id,
    )
    db.session.add(post)
    db.session.commit()

    data = {
        'status': 200,
        'msg': str(post.title) + ' created.' ,
    }

    return data

#delete post
@post_bp.route('/api/post/delete/', methods=['DELETE'])
@login_required
def delete_post():
    """
    Deletes Post
    """
    id = request.form['id']
    post = Post.query.get(id)
    if post is None:
        """
        abort(404) returns an error
        i think crafting a data response with a 404 error code returned will work
        """
        abort(404)
    
    db.session.delete(post)
    db.session.commit()
    data = {
        'status': 200,
        'msg': str(post.title) + ' deleted.'
    }

    return data

#update posts
@post_bp.route('/api/post/update/', methods=['PUT'])
@login_required
def update_post():
    """
    Updates Post
    """
    id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    post = Post.query.get(id)
            
    post.title = title
    post.content = content

    db.session.commit()
            
    data = {
    'status': 200,
    'title': post.title,
    'content': post.content,
    'msg': str(post.title) + ' created.'
    }

    return data

#like post
@post_bp.route('/api/post/like/<int:id>/', methods=['POST'])
@login_required
def likePost(id):
    """
    Logic to like user posts.
    Note** Remember to add a 'like' counter++
    """
    post = Post.query.get(id)
    if Post is None:

        data = {
            'status': 404,
            'msg': 'No post found with that id.'
        }
        return data
    
    else:
        like = Likes.query.get(id)
       
        

        db.session.add(id)
        db.session.count(id)
        db.session.commit()

        data = {
            'status': 200,
            'title': post.title,
            'msg': str(like.id) + ' liked this post.',
            'msg': str(like.created_on) + ' : date created.'

        }
        return data

#comment on a post
@post_bp.route('/api/post/comment/<int:id>/<action>', methods=['POST'])
@login_required
def commentPost():
    """
    Logic for commenting on a post.
    """
    pass



