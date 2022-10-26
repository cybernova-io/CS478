from flask import Blueprint
from flask_login import current_user, login_required
import os
from api.models.db import db
from ..models.Feed import Feed
from ..models.Users import User
from ..models.Posts import Post,PostComment,PostLike


feed_bp = Blueprint("feed_bp", __name__)

@feed_bp.get("/api/feed")
@login_required
def display_user_feed():
    #data = {}
    friend = current_user.friend
    if current_user.is_friend():
        user_feed = Post.query.all()
        user_feed.append([x.serialize() for x in i.posts])
    return user_feed

    
    