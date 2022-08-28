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