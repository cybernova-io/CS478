from datetime import datetime
from flask import Blueprint
from flask_login import current_user, login_required
from datetime import  datetime
from ..models.Posts import Post,PostComment,PostLike
from flask import (
    Blueprint,
    jsonify,
)

feed_bp = Blueprint("feed_bp", __name__)

@feed_bp.get("/api/feed")
@login_required
def display_user_feed():

    user_feed = []
    friends = current_user.friends

    for i in friends:

        user_feed.append([x.serialize() for x in i.posts])
        
        #user_feed = Post.query.order_by(Post.date_created.desc())

    return jsonify(user_feed)

    
    