"""Initialize app."""
from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
import logging
from api.models.Users import User, Role
from api.models.db import db
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_bootstrap import Bootstrap5


PROFILE_PICS = "api/static/profile-pics"
UPLOADS = "api/uploads"

jwt = JWTManager()



def create_app(config):
    """Construct the core app object."""
    app = Flask(__name__)

    if config == "dev":
        # Application Configuration
        app.config.from_object("config.DevConfig")
        app.config["PROFILE_PICS"] = PROFILE_PICS
        app.config["UPLOADS"] = UPLOADS
        app.config["MESSAGES_PER_PAGE"] = 10

        # JWT Config
        app.config["JWT_COOKIE_SECURE"] = False
        app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
        app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
        app.config["JWT_COOKIE_CSRF_PROTECT"] = False
        app.config["WTF_CSRF_ENABLED"] = True

    if config == "test":
        app.config.from_object("config.TestConfig")
    else:
        # change to prod for deployment
        app.config.from_object("config.DevConfig")

    # authentication
    app.config["LOGIN_DISABLED"] = True

    # Initialize Plugins
    db.init_app(app)
    jwt.init_app(app, add_context_processor=True)
    bootstrap = Bootstrap5(app)


    # Set up logging
    logging.basicConfig(
        filename="record.log",
        level=logging.DEBUG,
        format=f"%(asctime)s %(levelname)s %(name)s : %(message)s",
        filemode="w+",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    with app.app_context():

        from .routes.auth import auth_bp
        from .routes.app import app_bp
        from .routes.post import post_bp
        from .routes.friends import friend_bp
        from .routes.message import message_bp
        from .routes.profile import profile_bp
        from .routes.role import role_bp
        from .routes.feed import feed_bp
        from .routes.event import event_bp
        from .routes.block_user import blocked_bp
        from .routes.group import group_bp

        # Register Blueprints

        app.register_blueprint(auth_bp)
        app.register_blueprint(app_bp)
        app.register_blueprint(post_bp)
        app.register_blueprint(friend_bp)
        app.register_blueprint(message_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(role_bp)
        app.register_blueprint(feed_bp)
        app.register_blueprint(event_bp)
        app.register_blueprint(blocked_bp)
        app.register_blueprint(group_bp)
        # Create Database Models
        db.create_all()

        # Compile static assets

        return app
