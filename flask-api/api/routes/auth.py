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







