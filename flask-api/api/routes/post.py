from os import abort
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from ..models import db, Post
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

    try:
        id = request.form['id']
        
        post = Post.query.get(id)
        data = {
            'status': 200,
            'title': post.title,
            'content': post.content
        }
        return data

    except werkzeug.exceptions.BadRequestKeyError:
        posts = Post.query.all()
        for i in posts:
            data[i.id] = {
                'status': 200,
                'title': i.title,
                'content': i.content
            }
        return data


@post_bp.route('/api/post/<int:id>/', methods=['GET'])
def get_singlePost(id):
    """
    GET: return specific post of individual user 
    """
    data = {}

    id = request.form['id']
    post = Post.query.get(id)

    if id == id:
        data = {
            'status': 200,
            'title': post.title,
            'content': post.content
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



#delete function
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
    try:

            id = request.form['id']
            title = request.form['title']
            content = request.form['content']
            post = Post.query.get(id)

            # we already have the post object, i think you just want to update the attributes
            # ex. post.title = title
            # person submitting the update request should be the owner of the post, dont need to update id
            
            post = Post(
                title = title,
                content = content,
                owner = current_user.id,
            )
            
            #what are these doing here?
            title = request.form['title',Post.title]
            content = request.form['content',Post.content]

            #i dont think you need the update part. check out the flask-sqlalchemy documentation
            db.session.update(post)
            db.session.commit()
            #in our data responses, try to include a 'msg': with an explanation of what happened. easier for me to remember lol
            data = {
                'status': 200,
                'title': post.title,
                'content': post.content
            }

            return data
    
    #i dont think you need this exception, it was a quick hack to make the get function work
    except werkzeug.exceptions.BadRequestKeyError:
        if post is None:
            abort(404)
        data = {
            'status': 200,
            'title': post.title,
            'content': post.content
        }

        return data