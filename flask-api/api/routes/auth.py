from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory
from flask_login import login_required, logout_user, current_user, login_user
from ..models import db, User
from .. import login_manager
from flask_login import logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app as app


auth_bp = Blueprint('auth_bp', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/api/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests handle user creation.
    """

    """
    Sign-Up Form:
    name = Username associated with new account.
    email = User email associated with new account.
    password = Password associated with new account.
    """

    if request.method == 'GET':
        pass
    
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            user = User(
                name= name,
                email= email
            )

            user.set_password(password)
            user.set_creation_date()
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            data = {
                'status': 201,
                'msg': 'New user ' + user.name + ' created.'
            }

            return data

        data = {
            'status': 400,
            'msg': 'User with that email already exists.'
        }

        return data
    

@auth_bp.route('/api/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.

    Login Form

    email = email associated with existing account
    password = password associated with existing account
    next_page (not implemented yet) = page user was trying to access before they were prompted to login
    """

    if request.method == 'GET':
        data = {
            'status': 400,
            'msg': 'No user logged in.'
        }
        return data

    if request.method == 'POST':
        # Bypass if user is logged in
        if current_user.is_authenticated:
            data = {
                'status': 400,
                'msg': str(current_user.name) + ' already logged in.' 
            }
            return data

        
        email = request.form['email']
        password = request.form['password']
        #next_page = request.form['next_page']

        # Validate login attempt
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password=password):
            #User exists and password matches password in db
    
            login_user(user)
            data = {
                'status': 200,
                'msg': str(user.name) + ' logged in.'
            }

            user.set_last_login()
            
            return data
        #User exists but password does not match password in db
        data = {
            'status': 400,
            'msg': 'Invalid username/password combination'
        }
        
        #Return already logged in status message
        return data


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route("/api/logout", methods=['GET'])
@login_required
def logout():
    """User log-out logic."""

    data = {
        'status': 200,
        'msg': str(current_user.name) + ' logged out.'
    }

    logout_user()

    return data

@auth_bp.route('/api/profile', methods = ['GET'])
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
    
@auth_bp.route('/api/profile-picture/', methods= ['GET', 'POST'])
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






