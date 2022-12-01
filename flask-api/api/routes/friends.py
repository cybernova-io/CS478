from flask import (
    Blueprint,
    request,
    jsonify,
)
from flask_jwt_extended import current_user, jwt_required
from ..models.Users import db, User, pending_friend
from ..services.WebHelpers import WebHelpers
import logging

friend_bp = Blueprint("friend_bp", __name__)


@friend_bp.route("/api/friends/request/", methods=["POST"])
@jwt_required()
def add_friend():
    """
    POST: Allows a user to send a friend request to another user. The users then have a relationship in pending_friends.

    Form:

    friend_id = id of user being added as a friend.
    """

    data = {}
    friend_id = int(request.form["friend_id"])
    friend = User.query.get(friend_id)

    # check for no id passed for friend
    if friend is None:
        return WebHelpers.EasyResponse("Specified user does not exist.", 404)
    # check if id passed is current user
    if friend.id == current_user.id:
        return WebHelpers.EasyResponse("You cannot add yourself as a friend.", 400)
    # check if pending friend request already exists
    if friend.id in map(
        lambda pending_friend: pending_friend.id, current_user.pending_friends
    ):
        return WebHelpers.EasyResponse("Pending friend request already exists.", 400)
    # check if user is already friends with pending friend
    if friend.id in map(lambda pending_friend: pending_friend.id, current_user.friends):
        return WebHelpers.EasyResponse("You are already friends with this user.", 400)

    added = current_user.add_friend(friend)
    friend_added = friend.add_friend(current_user)
    # check to make sure friend was added to user object
    if added is None:

        return WebHelpers.EasyResponse("Error in adding friend.", 400)

    if friend_added is None:

        return WebHelpers.EasyResponse("Error in adding friend.", 400)

    # dont think i need the add here
    db.session.add(added)
    db.session.add(friend_added)
    db.session.commit()
    logging.info(f"{current_user.id} sent friend request to {friend.id}.")

    return WebHelpers.EasyResponse("Friend request sent to " + friend.username, 201)


@friend_bp.route("/api/friends/unfriend/", methods=["DELETE"])
@jwt_required()
def remove_friend():
    """
    DELETE: Allows user to delete a user that is currently their friend.

    Form:

    friend_id = id of friend being deleted from current_user
    """

    data = {}
    friend_id = request.form["friend_id"]
    friend = User.query.get(friend_id)

    # check for no id passed for friend
    if friend is None:
        return WebHelpers.EasyResponse("Specified user does not exist.", 404)
    # check if id passed is current user
    if friend.id == current_user.id:
        return WebHelpers.EasyResponse("You cannot remove yourself as friend.", 400)

    removed = current_user.remove_friend(friend)
    friend_removed = friend.remove_friend(current_user)
    # check to make sure friend was added to user object
    if removed is None:
        return WebHelpers.EasyResponse(
            "You are not currently friends with this user.", 400
        )
    if friend_removed is None:
        return WebHelpers.EasyResponse(
            "You are not currently friends with this user.", 400
        )

    # not sure if i need the add
    db.session.add(removed)
    db.session.add(friend_removed)
    db.session.commit()

    return WebHelpers.EasyResponse(
        "You are no longer friends with " + friend.username + ".", 200
    )


@friend_bp.route("/friends", methods=["GET"])
@jwt_required()
def get_friends_page():
    """
    GET: Returns all friends of current user.
    """

    friends = current_user.friends
    data = {}

    if friends.count() == 0:

        return WebHelpers.EasyResponse(current_user.username + "has no friends.", 400)

    data = [x.serialize() for x in friends]

    resp = jsonify(data)
    resp.status_code = 200

    return resp

@friend_bp.route("/api/friends/", methods=["GET"])
@jwt_required()
def get_friends():
    """
    GET: Returns all friends of current user.
    """

    friends = current_user.friends
    data = {}

    if friends.count() == 0:

        return WebHelpers.EasyResponse(current_user.username + "has no friends.", 400)

    data = [x.serialize() for x in friends]

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@friend_bp.route("/api/friends/pending-friends", methods=["GET"])
@jwt_required()
def get_pending_friends():
    """
    GET: Returns all pending friends of current user.
    """

    pending_friends = current_user.pending_friends
    data = {}

    if pending_friends.count() == 0:
        return WebHelpers.EasyResponse(
            current_user.userusername + "has no pending friends.", 400
        )

    data = [x.serialize() for x in pending_friends]

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@friend_bp.route("/api/friends/accept/", methods=["PUT"])
@jwt_required()
def accept_pending_friend(id):
    """
    GET: Allows current user to accept or decline a pending friend request.
    POST:
    """

    data = {}

    if request.method == "PUT":

        pending_friends = current_user.pending_friends
        pending_friend = User.query.get(id)

        if pending_friend == None:
            return WebHelpers.EasyResponse("The friend to add does not exist.", 400)
        if current_user.is_requestor(pending_friend) == True:
            return WebHelpers.EasyResponse(
                "You cannot accept your own sent friend request.", 400
            )
        if pending_friends.count() == 0:
            return WebHelpers.EasyResponse(
                current_user.username + "has no pending friends.", 400
            )

        if id in map(lambda pending_friend: pending_friend.id, pending_friends):

            added = current_user.add_pending_friend(pending_friend)
            friend_added = pending_friend.add_pending_friend(current_user)

            if added is None:
                return WebHelpers.EasyResponse("Error in adding friend.", 400)

            # not sure if add is needed
            db.session.add(added)
            db.session.add(friend_added)
            db.session.commit()

            return WebHelpers.EasyResponse(
                str(pending_friend.username) + "'s friend request accepted.", 200
            )
        return WebHelpers.EasyResponse("Specified user is not a pending friend. ", 200)


@friend_bp.route("/api/friends/reject/", methods=["DELETE"])
@jwt_required()
def decline_pending_friend(id):

    pending_friends = current_user.pending_friends
    pending_friend = User.query.get(id)

    if pending_friends.count() == 0:
        return WebHelpers.EasyResponse(
            current_user.username + " has no pending friends.", 400
        )
    if pending_friend == None:
        return WebHelpers.EasyResponse("The friend to add does not exist.", 400)

    if id in map(lambda pending_friend: pending_friend.id, pending_friends):
        removed = current_user.remove_pending_friend(pending_friend)
        friend_removed = pending_friend.remove_pending_friend(current_user)

        db.session.commit()

        if removed is None:
            return WebHelpers.EasyResponse("Error in declining friend request.", 400)
        if friend_removed is None:
            return WebHelpers.EasyResponse("Error in declining friend request.", 400)

        return WebHelpers.EasyResponse(
            pending_friend.username + "'s friend request declined.", 400
        )


@friend_bp.route("/api/friends/friend-suggestions", methods=["GET"])
@jwt_required()
def get_friend_suggestions():
    """
        RETURNS A LIST OF SUGGESTED FRIENDS
    """ 
    data = {}
    users = User.query.all()
    friends = current_user.friends

    for x in friends: 
        if x == friends:
            return WebHelpers.EasyResponse(
            current_user.userusername + "Users are currently friends.", 400
        )
    data = [x.serialize() for x in users]
    resp = jsonify(data)
    resp.status_code = 200
    return resp


   



   

    