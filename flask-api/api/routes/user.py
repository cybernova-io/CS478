from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory, jsonify, Response
from flask_login import login_required, logout_user, current_user, login_user
from ..models.Users import db, User, pending_friend
from .. import login_manager
from flask_login import logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app as app
from sqlalchemy import engine, create_engine
from ..services.WebHelpers import WebHelpers

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


user_bp = Blueprint('user_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/api/profile', methods = ['GET'])
@login_required
def profile():
    """
    GET: Returns all user attributes to be displayed in profile
    """
    data = {
        'user_id': current_user.id,
        'user_name': current_user.name,
        'user_email': current_user.email,
        'user_creation_date': current_user.created_on,
        'user_last_login': current_user.last_login
    }

    resp = jsonify(data)
    resp.status_code = 200

    return data

@user_bp.route('/api/profile-picture/', methods= ['GET', 'POST'])
@login_required
def profile_picture():
    """
    GET: Returns the current users profile picture.
    POST: Allows user to submit a picture to be used as their profile picture.

    Profile Picture Form

    picture = file to be used as profile picture. must be jpeg, jpg, or png
    """

    #request for just getting profile picture
    if request.method == 'GET':
        if current_user.profile_pic is not None:
            path = current_user.profile_pic
            path = 'profile-pics/' + path
            return send_from_directory('static', path)
        else:

            return WebHelpers.EasyResponse('User has no profile picture.', 400)

    if request.method == 'POST':
        #check if request has the file part
        if 'picture' not in request.files:
            
            return WebHelpers.EasyResponse('No picture provided.', 400)

        picture = request.files['picture']

        #make sure filename is not empty
        if picture.filename == '':

            return WebHelpers.EasyResponse('No picture provided.', 400)
        
        #make sure picture exists, and file extension is in allowed extensions
        if picture and allowed_file(picture.filename):
            
            filename = secure_filename(picture.filename)
            filename = str(current_user.id) + '_' + filename
            
            picture.save(os.path.join(app.config['PROFILE_PICS'], filename))
            current_user.profile_pic = filename
            db.session.commit()

            return WebHelpers.EasyResponse('Profile picture uploaded.', 200)

@user_bp.route('/api/add-friend/', methods = ['POST'])
@login_required
def add_friend():
    """
    POST: Allows a user to send a friend request to another user. The users then have a relationship in pending_friends.

    Form:

    friend_id = id of user being added as a friend.
    """

    data = {}
    friend_id = int(request.form['friend_id'])
    friend = User.query.get(friend_id)

    # check for no id passed for friend
    if friend is None:

        return WebHelpers.EasyResponse('Specified user does not exist.', 404)
    #check if id passed is current user
    if friend.id == current_user.id:
        return WebHelpers.EasyResponse('You cannot add yourself as a friend.', 400)

    #check if pending friend request already exists
    if friend.id in map(lambda pending_friend: pending_friend.id, current_user.pending_friends):
        
        return WebHelpers.EasyResponse('Pending friend request already exists.', 400)

    #check if user is already friends with pending friend
    if friend.id in map(lambda pending_friend: pending_friend.id, current_user.friends):
        
        return WebHelpers.EasyResponse('You are already friends with this user.', 400)


    added = current_user.add_friend(friend)
    friend_added = friend.add_friend(current_user)
    #check to make sure friend was added to user object
    if added is None:
        
        return WebHelpers.EasyResponse('Error in adding friend.', 400)

    if friend_added is None:
        
        return WebHelpers.EasyResponse('Error in adding friend.', 400)

    # dont think i need the add here
    db.session.add(added)
    db.session.add(friend_added)
    db.session.commit()

    return WebHelpers.EasyResponse('Friend request sent to ' + friend.name, 201)


@user_bp.route('/api/remove-friend/', methods = ['DELETE'])
@login_required
def remove_friend():
    """
    DELETE: Allows user to delete a user that is currently their friend.

    Form:

    friend_id = id of friend being deleted from current_user
    """

    data = {}
    friend_id = request.form['friend_id']
    friend = User.query.get(friend_id)

    # check for no id passed for friend
    if friend is None:
        
        return WebHelpers.EasyResponse('Specified user does not exist.', 404)

    #check if id passed is current user
    if friend.id == current_user.id:
        
        return WebHelpers.EasyResponse('You cannot remove yourself as friend.', 400)
        
    removed = current_user.remove_friend(friend)
    friend_removed = friend.remove_friend(current_user)
    #check to make sure friend was added to user object
    if removed is None:
        
        return WebHelpers.EasyResponse('You are not currently friends with this user.', 400)

    if friend_removed is None:
        
        return WebHelpers.EasyResponse('You are not currently friends with this user.', 400)

    #not sure if i need the add
    db.session.add(removed)
    db.session.add(friend_removed)
    db.session.commit()

    return WebHelpers.EasyResponse('You are no longer friends with ' + friend.name + '.', 200)

@user_bp.route('/api/friends/', methods = ['GET'])
def get_friends():
    """
    GET: Returns all friends of current user.
    """

    friends = current_user.friends
    data = {}
    
    if friends.count() == 0:

        return WebHelpers.EasyResponse(current_user.name + 'has no friends.', 400)

    for i in friends:
        data['friend'] = i.serialize()
    resp = jsonify(data)
    resp.status_code = 200

    return resp

@user_bp.route('/api/friends/pending-friends/', methods = ['GET'])
def get_pending_friends():
    """
    GET: Returns all pending friends of current user.
    """

    pending_friends = current_user.pending_friends
    data = {}
    
    if pending_friends.count() == 0:
        data = {
            'msg': current_user.name + ' has no pending friends.' 
        }
        resp = jsonify(data)
        resp.status_code = 400
        return resp

    for i in pending_friends:
        data['friend_request'] = i.serialize()
    resp = jsonify(data)
    resp.status_code = 200

    return resp

@user_bp.route('/api/friends/pending-friends/<string:action>/<int:id>', methods = ['GET', 'POST'])
def handle_pending_friend(action, id):
    """
    GET: Allows current user to accept or decline a pending friend request.
    POST:
    """

    data = {}

    if request.method == 'GET':

        if action == 'accept':

            pending_friends = current_user.pending_friends
            pending_friend = User.query.get(id)

            if pending_friend == None:
                return WebHelpers.EasyResponse('The friend to add does not exist.', 400)
                

            if current_user.is_requestor(pending_friend) == True:
            
                return WebHelpers.EasyResponse('You cannot accept your own sent friend request.', 400)

            if pending_friends.count() == 0:
                
                return WebHelpers.EasyResponse(current_user.name + 'has no pending friends.', 400)

            if id in map(lambda pending_friend: pending_friend.id, pending_friends):

                added = current_user.add_pending_friend(pending_friend)
                friend_added = pending_friend.add_pending_friend(current_user)

                if added is None:
                    return WebHelpers.EasyResponse('Error in adding friend.', 400)

                #not sure if add is needed
                db.session.add(added)
                db.session.add(friend_added)
                db.session.commit()
                
                return WebHelpers.EasyResponse(pending_friend.name + '\'s friend request accepted.', 200)

        elif action == 'decline':
            pending_friends = current_user.pending_friends
            pending_friend = User.query.get(id)

            if pending_friends.count() == 0:
                
                return WebHelpers.EasyResponse(current_user.name + ' has no pending friends.', 400)

            if pending_friend == None:
                
                return WebHelpers.EasyResponse('The friend to add does not exist.', 400)
            
            if id in map(lambda pending_friend: pending_friend.id, pending_friends):
                removed = current_user.remove_pending_friend(pending_friend)
                friend_removed = pending_friend.remove_pending_friend(current_user)
                
                db.session.commit()

                if removed is None:
                    
                    return WebHelpers.EasyResponse('Error in declining friend request.', 400)

                if friend_removed is None:
                    
                    return WebHelpers.EasyResponse('Error in declining friend request.', 400)
                

                return WebHelpers.EasyResponse(pending_friend.name + '\'s friend request declined.', 400)



            
        
        
            