from flask import (
    Blueprint,
    request,
    send_from_directory,
    jsonify,
    render_template,
    redirect
)
from ..models.Users import db, User, pending_friend
from flask_jwt_extended import jwt_required, current_user
from flask import current_app as app
from ..services.WebHelpers import WebHelpers
from api.models.Events import Event, event_attendees
import logging

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods = ['GET', 'POST'])
@jwt_required()
def profile_page():
    """
    GET: Returns all user attributes to be displayed in profile. This is how logged in users can view their profile.
    """
    events = Event.query.filter_by(owner_id = current_user.id).all()
    #attending 
    if request.method == 'GET':
        data = {
            "username": current_user.username,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "major": current_user.major,
            "grad_year": current_user.grad_year,
            "email": current_user.email,
            "creation_date": current_user.created_on,
            "last_login": current_user.last_login,
            "pending_friends": [x.username for x in current_user.pending_friends],
            "friends": [x.username for x in current_user.friends],
            "posts": current_user.posts,
            "groups": current_user.groups,
            "events": events
        }

        return render_template("/profile/my-profile.html", data=data)
    if request.method == 'POST':
        user : User

        user = User.query.get(current_user.id)

        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.major = request.form['major']
        user.grad_year = request.form['grad_year']
        user.email = request.form['email']

        db.session.commit()
        return redirect('/profile')


@profile_bp.get("/profile/<int:id>")
@jwt_required()
def friend_profile_page(id):
    """
    GET: Returns all user attributes to be displayed in profile. This is how logged in users can view their profile.
    """

    user : User

    user = User.query.get(id)

    data = {
        "user_username": user.username,
        "user_first_name": user.first_name,
        "user_last_name": user.last_name,
        "user_major": user.major,
        "user_grad_year": user.grad_year,
        "user_email": user.email,
        "user_creation_date": user.created_on,
        "user_last_login": user.last_login,
        "pending_friends": [x.username for x in user.pending_friends],
        "friends": [x.username for x in user.friends],
    }

    resp = jsonify(data)
    resp.status_code = 200

    return data


######################################################### API BELOW, SERVER RENDERING ABOVE


@profile_bp.get("/api/profile")
@jwt_required()
def profile():
    """
    GET: Returns all user attributes to be displayed in profile. This is how logged in users can view their profile.
    """

    data = {
        "user_username": current_user.username,
        "user_first_name": current_user.first_name,
        "user_last_name": current_user.last_name,
        "user_major": current_user.major,
        "user_grad_year": current_user.grad_year,
        "user_email": current_user.email,
        "user_creation_date": current_user.created_on,
        "user_last_login": current_user.last_login,
        "pending_friends": [x.username for x in current_user.pending_friends],
        "friends": [x.username for x in current_user.friends],
    }

    resp = jsonify(data)
    resp.status_code = 200

    return data


@profile_bp.get("/api/profile/<string:username>")
@jwt_required()
def lookup_profile(username):
    """
    GET: Allows user to search other profiles
    """
    user = User.query.filter_by(username=username).first()

    if user is None:
        return WebHelpers.EasyResponse("Specified user does not exist.", 404)
    else:
        data = {
            "user_username": user.username,
            "user_name": user.name,
            "friends": [x.username for x in user.friends],
        }

        resp = jsonify(data)
        resp.status_code = 200

        return data


@profile_bp.put("/api/profile")
@jwt_required()
def edit_profile():
    """
    PUT: Allows user to modify their profile attributes.
    """
    username = request.form["username"]
    name = request.form["name"]
    email = request.form["email"]

    if User.query.filter_by(username=username).first() is None:
        current_user.username = username
        current_user.name = name
        current_user.email = email
        db.session.commit()

        data = {
            "user_username": current_user.username,
            "user_name": current_user.name,
            "user_email": current_user.email,
            "user_creation_date": current_user.created_on,
            "user_last_login": current_user.last_login,
            "pending_friends": [x.username for x in current_user.pending_friends],
            "friends": [x.username for x in current_user.friends],
        }

        resp = jsonify(data)
        resp.status_code = 200

        return data

    else:
        return WebHelpers.EasyResponse("That username is taken!", 400)


@profile_bp.route("/api/profile-picture", methods=["GET", "POST"])
@jwt_required()
def profile_picture():
    """
    GET: Returns the current users profile picture.
    POST: Allows user to submit a picture to be used as their profile picture.

    Profile Picture Form

    picture = file to be used as profile picture. must be jpeg, jpg, or png
    """

    # request for just getting profile picture
    if request.method == "GET":
        if current_user.profile_pic is not None:
            path = current_user.profile_pic
            path = "profile-pics/" + path
            return send_from_directory("static", path)
        else:

            return WebHelpers.EasyResponse("User has no profile picture.", 400)

    if request.method == "POST":
        return WebHelpers.HandleUserPictureUpload("PROFILE_PICS")


@profile_bp.get("/api/users/<int:id>")
@jwt_required()
def user_details(id):

    user = User.query.get(id)

    if user is not None:

        return {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "userId": user.id,
        }
    else:
        return WebHelpers.EasyResponse(f"User not found with id {id}.", 404)
