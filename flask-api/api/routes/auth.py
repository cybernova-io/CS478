from flask import (
    Blueprint,
    redirect,
    flash,
    request,
    url_for,
)
from flask_login import login_required
from flask_security import login_required, current_user, login_user
from flask_security.utils import verify_password, hash_password
from ..models.Users import db, User
from .. import login_manager
from flask_login import logout_user
from ..services.WebHelpers import WebHelpers
import logging
from api import user_datastore
from flask import current_app as app

auth_bp = Blueprint("auth_bp", __name__)
login_manager = app.login_manager

@auth_bp.post("/api/signup")
def signup():
    """
    User sign-up page.
    """

    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    major = request.form["major"]
    grad_year = request.form["gradYear"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    existing_user = user_datastore.find_user(email=email)

    if existing_user is None:
        password = hash_password(password)
        user = user_datastore.create_user(
            first_name=first_name,
            last_name=last_name,
            major=major,
            password=password,
            grad_year=grad_year,
            username=username,
            email=email,
        )

        db.session.commit()  # Create new user
        logging.info("New user created - " + str(user.id) + " - " + str(user.username))
        login_user(user)  # Log in as newly created user

        return WebHelpers.EasyResponse("New user " + user.username + " created.", 201)

    return WebHelpers.EasyResponse("User with that email already exists. ", 400)


@auth_bp.post("/api/login")
def login():
    """
    Log-in page for registered users.
    """

    # Bypass if user is logged in
    if current_user.is_authenticated:
        return WebHelpers.EasyResponse(current_user.username + " already logged in.", 400)

    email = request.form["email"]
    password = request.form["password"]
    # next_page = request.form['next_page']

    # Validate login attempt
    user = user_datastore.find_user(email=email)
    password_matches = verify_password(password, user.password)

    if user:
        if user and password_matches:
            # User exists and password matches password in db
            login_user(user)
            user.set_last_login()
            return WebHelpers.EasyResponse(user.username + " logged in.", 200)


    # User exists but password does not match password in db
    return WebHelpers.EasyResponse("Invalid username/password combination.", 405)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return WebHelpers.EasyResponse("You must login to view this page", 401)


@auth_bp.route("/api/logout", methods=["GET"])
@login_required
def logout():
    """User log-out logic."""

    username = current_user.username
    logout_user()
    return WebHelpers.EasyResponse(username + " logged out.", 200)
