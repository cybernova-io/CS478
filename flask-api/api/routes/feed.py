from flask import Blueprint
from flask_login import current_user, login_required
from ..models.Feed import Feed
from ..models.Users import User

feed_bp = Blueprint("feed_bp", __name__)

@feed_bp.get('/api/feed')
@login_required
def get_feed():

    

