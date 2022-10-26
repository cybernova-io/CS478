from flask import Blueprint
from flask_login import current_user, login_required
import os
import json
from api.models.db import db
#from ..models.Feed import Feed
from ..models.Users import User
from ..models.Posts import Post,PostComment,PostLike
from flask import (
    Blueprint,
    redirect,
    render_template,
    flash,
    request,
    session,
    url_for,
    jsonify,
    Response,
)
from ..services.WebHelpers import WebHelpers

feed_bp = Blueprint("feed_bp", __name__)



@feed_bp.get("/api/feed")
@login_required
def display_user_feed():
    user_feed = {}
    friends = current_user.friend
    for i in friends:
        user_feed.append([x.serialize() for x in i.posts])
    return user_feed

    
    