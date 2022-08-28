from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory, jsonify
from flask_login import login_required, logout_user, current_user, login_user
from ..models import db, User
from .. import login_manager
from flask_login import logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app as app


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
        'status': 200,
        'user_id': current_user.id,
        'user_name': current_user.name,
        'user_email': current_user.email,
        'user_creation_date': current_user.created_on,
        'user_last_login': current_user.last_login
    }

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
            return None

    if request.method == 'POST':
        #check if request has the file part
        if 'picture' not in request.files:
            data = {
                'status': 404,
                'msg': 'No picture provided.'
            }
            return data

        picture = request.files['picture']

        #make sure filename is not empty
        if picture.filename == '':
            data = {
                'status': 404,
                'msg': 'Picture provided has no filename.'
            }
            return data
        
        #make sure picture exists, and file extension is in allowed extensions
        if picture and allowed_file(picture.filename):
            
            filename = secure_filename(picture.filename)
            filename = str(current_user.id) + '_' + filename
            
            picture.save(os.path.join(app.config['PROFILE_PICS'], filename))
            current_user.profile_pic = filename
            db.session.commit()

            data = {
                'status': 200,
                'msg': 'Profile picture uploaded.'
            }

            return data

@user_bp.route('/api/add-friend/', methods = ['POST'])
@login_required
def add_friend():

    data = {}
    friend_id = request.form['friend_id']
    friend = User.query.get(friend_id)

    # check for no id passed for friend
    if friend is None:
        data = {
            'status': 404,
            'msg': 'Specified user does not exist.'
        }
        return data

    #check if id passed is current user
    if friend.id == current_user.id:
        data = {
            'status': 404,
            'msg': 'You cannot add yourself as a friend.'
        }
        return data

    added = current_user.add_friend(friend)

    #check to make sure friend was added to user object
    if added is None:
        data = {
            'status': 404,
            'msg': 'Error in adding friend.'
        }
        return data
    db.session.add(added)
    db.session.commit()

    data = {
        'status': 200,
        'msg': 'You are now friends with ' + friend.name + '.'
    }

    return data

@user_bp.route('/api/remove-friend/', methods = ['DELETE'])
@login_required
def remove_friend():

    data = {}
    friend_id = request.form['friend_id']
    friend = User.query.get(friend_id)

    # check for no id passed for friend
    if friend is None:
        data = {
            'status': 404,
            'msg': 'Specified user does not exist.'
        }
        return data

    #check if id passed is current user
    if friend.id == current_user.id:
        data = {
            'status': 404,
            'msg': 'You cannot remove yourself as a friend.'
        }
        return data

    
    removed = current_user.remove_friend(friend)
    
    #check to make sure friend was added to user object
    if removed is None:
        data = {
            'status': 404,
            'msg': 'You are not currently friends with this user.'
        }
        return data

    db.session.add(removed)
    db.session.commit()

    data = {
        'status': 200,
        'msg': 'You are no longer friends with ' + friend.name + '.'
    }

    return data

@user_bp.route('/api/friends/', methods = ['GET'])
def get_friends():

    friends = current_user.friends
    data = {}
    
    for i in friends:
        data['friend'] = i.serialize()

    return data