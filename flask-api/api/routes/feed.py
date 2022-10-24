from flask import Blueprint
from flask_login import current_user, login_required
from ..models.Feed import Feed
from ..models.Users import User
from ..models.Posts import Post
from ..models.Posts import PostComment
from ..models.Posts import PostLike

feed_bp = Blueprint("feed_bp", __name__)

@feed_bp.get('/api/feed', methods='GET')
@login_required
def display_user_feed():
    friends = current_user.friends
    return friends