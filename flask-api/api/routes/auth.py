from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory, Response, jsonify
from flask_login import login_required, logout_user, current_user, login_user
from ..models.Users import db, User
from .. import login_manager
from flask_login import logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app as app
from ..services.WebHelpers import WebHelpers
import logging

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    """
    User sign-up page.
    POST requests handle user creation.
    """

    """
    Sign-Up Form:
    name = Username associated with new account.
    email = User email associated with new account.
    password = Password associated with new account.
    """

    if request.method == 'POST':

        first_name = request.form['firstName']
        last_name = request.form['lastName']
        major = request.form['major']
        grad_year = request.form['gradYear']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user is None:
            user = User(
                first_name=first_name,
                last_name=last_name,
                major=major,
                grad_year=grad_year,
                username=username,
                email= email
            )

            user.set_password(password)
            user.set_creation_date()
            db.session.add(user)
            db.session.commit()  # Create new user
            logging.info('New user created - ' + str(user.id) + ' - ' + str(user.username))
            login_user(user)  # Log in as newly created user
            
            return WebHelpers.EasyResponse('New user ' + user.username + ' created.' , 201)

        return WebHelpers.EasyResponse('User with that email already exists. ', 400)    

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
        return WebHelpers.EasyResponse('Login with POST method.', 405)

    if request.method == 'POST':
        # Bypass if user is logged in
        if current_user.is_authenticated:
            return WebHelpers.EasyResponse(current_user.name + ' already logged in.', 400)

        
        email = request.form['email']
        password = request.form['password']
        #next_page = request.form['next_page']

        # Validate login attempt
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password=password):
            #User exists and password matches password in db
    
            login_user(user)
            user.set_last_login()

            return WebHelpers.EasyResponse(user.name + ' logged in.' , 405)
            
        #User exists but password does not match password in db
        return WebHelpers.EasyResponse('Invalid username/password combination.', 405)


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

    name = current_user.name
    logout_user()

    return WebHelpers.EasyResponse(name + ' logged out.', 200)







