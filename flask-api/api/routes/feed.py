from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from flask import request
from ..models.Posts import Post
from api.models.Events import Event
from api.models.Users import Group
from api.models.Users import User
from api.services.WebUtils import WebUtils
from flask import (
    Blueprint,
    jsonify,
    render_template,
    flash
)
import random

feed_bp = Blueprint("feed_bp", __name__)

@feed_bp.get("/feed")
@jwt_required()
def feed_page():
    user_feed = []
    friends = current_user.friends
    events = Event.query.all()
    suggested_events = []
    data = []
    #could be list comprehension
    for friend in friends:
        for event in events:
            if event.owner_id == friend.id or event.in_event(friend) == True:
                if WebUtils.time_in_range_one_week(event.time):
                    if event.in_event(current_user) == False:
                        if event.serialize_feed() not in data:
                            data.append(event.serialize_feed())

    for i in friends:
        [data.append(x.serialize_feed()) for x in i.posts]
    random.shuffle(data)
    return render_template("/feed/feed.html", data=data)

@feed_bp.post("/search")
@jwt_required()
def search_page():

    category = request.form.get('category')
    search_term = request.form.get('search-term')

    if category == 'Users':

        users = User.query.filter(User.username.like("%" + search_term + "%")).all()
        data = [x.serialize_search() for x in users]
        print(data)

    elif category == 'Friends':
        pass
    elif category == 'Posts':
        posts = Post.query.filter(Post.title.like("%" + search_term + "%")).all()
        data = [x.serialize() for x in posts]
    elif category == 'Groups':
        groups = Group.query.filter(Group.name.like("%" + search_term + "%")).all()
        data = groups
    elif category == 'Events':
        events = Event.query.filter(Event.name.like("%" + search_term + "%")).all()
        data = events
    else:
        return None
    

    return render_template("/feed/search.html", data=data, data_type=category)


######################################################### API BELOW, SERVER RENDERING ABOVE

@jwt_required()
def create_feed():
    user_feed = []
    friends = current_user.friends
    for i in friends:
        user_feed.append([x.serialize() for x in i.posts])
    return user_feed

@feed_bp.get("/api/feed")
@jwt_required()
def display_user_feed():
    user_feed = []
    friends = current_user.friends
    

    for i in friends:
        user_feed.append([x.serialize() for x in i.posts])

    return jsonify(user_feed)



@feed_bp.get("/api/search/user/username")
@jwt_required()
def search_username():
    query = request.args.get("query")
    users = User.query.filter(User.username.like("%" + query + "%")).all()
    resp = jsonify([x.serialize_search() for x in users])
    return resp


@feed_bp.get("/api/search/user/major")
@jwt_required()
def search_major():
    query = request.args.get("query")
    users = User.query.filter(User.major.like("%" + query + "%")).all()
    resp = jsonify([x.serialize_search() for x in users])
    return resp


@feed_bp.get("/api/search/user/gradYear")
@jwt_required()
def search_grad_year():
    query = request.args.get("query")
    users = User.query.filter(User.grad_year.like("%" + query + "%")).all()
    resp = jsonify([x.serialize_search() for x in users])
    return resp


@feed_bp.get("/api/search/post/title")
@jwt_required()
def search_post_title():
    query = request.args.get("query")
    posts = Post.query.filter(Post.title.like("%" + query + "%")).all()
    resp = jsonify([x.serialize_search() for x in posts])
    return resp


@feed_bp.get("/api/search/post/text")
@jwt_required()
def search_post_text():
    query = request.args.get("query")
    posts = Post.query.filter(Post.content.like("%" + query + "%")).all()
    resp = jsonify([x.serialize_search() for x in posts])
    return resp
