from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory
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