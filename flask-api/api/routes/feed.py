from flask import Blueprint
from flask_login import current_user, login_required
from flask import request
from ..models.Posts import Post
from api.models.Users import User
from flask import (
    Blueprint,
    jsonify,
)
from ..services.WebHelpers import WebHelpers

feed_bp = Blueprint("feed_bp", __name__)

@feed_bp.get("/api/feed")
@login_required
def display_user_feed():
    user_feed = []
    friends = current_user.friends
    for i in friends:
        user_feed.append([x.serialize() for x in i.posts])
        user_feed = Post.query.order_by(Post.date_created.desc())
    return jsonify([x.serialize() for x in user_feed])


@feed_bp.get("/api/search/username/")
@login_required
def search_username():
    query = request.args.get("query")
    users = User.query.filter(User.username.like("%"+query+"%")).all()
    resp = jsonify([x.serialize_search() for x in users])
    return resp

@feed_bp.get("/api/search/major/")
@login_required
def search_major():
    query = request.args.get("query")
    users = User.query.filter(User.major.like("%"+query+"%")).all()
    resp = jsonify([x.serialize_search() for x in users])
    return resp

@feed_bp.get("/api/search/gradYear/")
@login_required
def search_grad_year():
    query = request.args.get("query")
    users = User.query.filter(User.grad_year.like("%"+query+"%")).all()
    resp = jsonify([x.serialize_search() for x in users])
    return resp
    
    