from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    make_response
)
from flask_security.utils import verify_password, hash_password
from ..models.Users import db, User
from flask_login import logout_user
from ..services.WebHelpers import WebHelpers
import logging
from api import user_datastore
from flask import current_app as app, jsonify
from flask_cors import cross_origin
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user, set_access_cookies
from api import jwt
from api.forms.SigninForm import SigninForm
from api.forms.SignupForm import SignupForm


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signin", methods = ["GET", "POST"])
def signin_page():
    form = SigninForm()
    if form.validate_on_submit():

        # Validate login attempt
        user = User.query.filter_by(email=form.email.data).one_or_none()
        password_matches = verify_password(form.password.data, user.password)

        if user:
            if user and password_matches:
                # User exists and password matches password in db
                user.set_last_login()
                access_token = create_access_token(identity=user)
                resp = make_response(render_template('feed.html'))

                set_access_cookies(resp, access_token)
                return resp
    return render_template("signin.html", form=form)

@auth_bp.route("/signup", methods = ["GET", "POST"])
def signup_page():
    form = SignupForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        major = form.major.data
        grad_year = form.grad_year.data
        username = form.username.data
        email = str(form.email.data).lower()
        password = form.password.data

        existing_user = User.query.filter_by(email=email).scalar()

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
            db.session.add(user)
            db.session.commit()  # Create new user
            logging.info("New user created - " + str(user.id) + " - " + str(user.username))
            access_token = create_access_token(identity=user)
            resp = make_response(render_template('feed.html'))

            set_access_cookies(resp, access_token)
            return resp

    return render_template('signup.html', form=form)


@cross_origin()
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
    email = request.form["email"].lower()
    password = request.form["password"]

    existing_user = User.query.filter_by(email=email).scalar()

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
        db.session.add(user)
        db.session.commit()  # Create new user
        logging.info("New user created - " + str(user.id) + " - " + str(user.username))
        access_token = create_access_token(identity=user)

        resp = {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "userId": user.id,
            "token": access_token,
        }

        set_access_cookies(resp, access_token)

        return resp

    return WebHelpers.EasyResponse("User with that email already exists. ", 400)


@cross_origin()
@auth_bp.post("/api/login")
def login():
    """
    Log-in page for registered users.
    """

    email = request.form["email"]
    password = request.form["password"]

    # Validate login attempt
    user = User.query.filter_by(email=email).one_or_none()
    password_matches = verify_password(password, user.password)

    if user:
        if user and password_matches:
            # User exists and password matches password in db
            user.set_last_login()
            # return WebHelpers.EasyResponse(user.username + " logged in.", 200)

            access_token = create_access_token(identity=user)

            resp = jsonify(
                {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "userId": user.id,
                    "token": access_token,
                }
            )
            set_access_cookies(resp, access_token)

            return resp

    # User exists but password does not match password in db
    return WebHelpers.EasyResponse("Invalid username/password combination.", 405)


@app.route("/me")
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        firstName=current_user.first_name,
        username=current_user.username,
    )


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


#
# @login_manager.user_loader
# def load_user(user_id):
#    """Check if user is logged-in on every page load."""
#    if user_id is not None:
#        return User.query.get(user_id)
#    return None


# @login_manager.unauthorized_handler
# def unauthorized():
#    """Redirect unauthorized users to Login page."""
#    return WebHelpers.EasyResponse("You must login to view this page", 401)


# @auth_bp.route("/api/logout", methods=["GET"])
# @login_required
# def logout():
#    """User log-out logic."""


@auth_bp.post("/api/grant_role")
def grant_role():
    """Add a role to a users account."""

    user_id = request.form["user_id"]
    role_name = request.form["role_name"]
    user = User.query.get(user_id)
    if user:
        user_datastore.add_role_to_user(user, role_name)
        db.session.commit()
        logging.warning(
            f"User id - {current_user.id} - granted {role_name} role to User id - {user_id} - "
        )
        return WebHelpers.EasyResponse("Role granted to user.", 200)
    return WebHelpers.EasyResponse("User with that id does not exist.", 404)


@auth_bp.post("/api/revoke_role")
def revoke_rule():
    """Remove a role from a users account."""

    user_id = request.form["user_id"]
    role_name = request.form["role_name"]

    user = User.query.get(user_id)
    if user:
        user_datastore.remove_role_from_user(user, role_name)
        db.session.commit()
        logging.warning(
            f"User id - {current_user.id} - revoked {role_name} role from User id - {user_id} -"
        )
        return WebHelpers.EasyResponse("Role revoked from user.", 200)
    return WebHelpers.EasyResponse("User with that id does not exist.", 404)


@auth_bp.get("/api/check_roles")
def check_roles():
    """Check a users roles."""

    user_id = request.form["user_id"]
    user = User.query.get(user_id)

    if user:
        roles = [x.serialize() for x in user.roles]
        logging.info(f"User id {current_user.id} accessed User id - {user_id} - roles")
        return roles

    username = current_user.username
    logout_user()
    return WebHelpers.EasyResponse(username + " logged out.", 200)
