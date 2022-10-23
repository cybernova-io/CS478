"""Flask app configuration."""
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class DevConfig:
    """Set Flask configuration from environment variables."""

    FLASK_APP = 'wsgi.py'
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/api/' 'development.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask-Security
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_TRACKABLE = environ.get('SECURITY_TRACKABLE')
    #SECURITY_LOGIN_URL = '/api/login'	
    SECURITY_REGISTERABLE = False
    LOGIN_DISABLED = False

class TestConfig:

    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345')
    SECURITY_PASSWORD_SALT = '1234566'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = False
    DEBUG = True