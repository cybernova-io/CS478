from flask import (
    Blueprint,
    redirect,
    render_template,
    flash,
    request,
    session,
    url_for,
    send_from_directory,
    jsonify,
    Response,
)
from flask_login import login_required, logout_user, current_user, login_user
from ..models.Users import db, User, pending_friend, Message
from .. import login_manager
from flask_login import logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app as app
from sqlalchemy import engine, create_engine
from ..services.WebHelpers import WebHelpers
import logging
from ..models.Notifications import Notification
from .message import Message

message_bp = Blueprint("message_bp", __name__)


@message_bp.route("/api/messages", methods=["GET"])
@login_required
def messages():

    if request.method == "GET":
        messages = Message.query.filter(
            (Message.sender_id == current_user.id)
            | (Message.recipient_id == current_user.id)
        ).all()

        data = jsonify([x.serialize() for x in messages])

        resp = data
        resp.status_code
        return data


@message_bp.route("/api/messages/<string:user>")
@login_required
def messages_user(user):

    if request.method == "GET":

        current_user.last_message_read_time = datetime.utcnow()
        current_user.add_notification("unread_message_count", 0)
        db.session.commit()

        data = {}

        friend = User.query.filter_by(username=user).first()

        if friend is None:
            return WebHelpers.EasyResponse("Specified user does not exist.", 404)

        # messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, app.config['MESSAGES_PER_PAGE'], False )
        messages = current_user.messages_received.where(
            Message.sender_id == friend.id
        ).all()

        if messages is None:
            return WebHelpers.EasyResponse("You have no messages with this user.", 400)

        data = [x.serialize() for x in messages]

        resp = jsonify(data)
        resp.status_code = 200

        return resp
    else:
        return WebHelpers.EasyResponse(
            "GET method should be used for retrieving messages.", 405
        )


@message_bp.route("/api/send-message/<recipient>", methods=["GET", "POST"])
@login_required
def send_message(recipient):
    """
    Allows user to send a private message to another user.

    GET:
    POST: Takes recipient name and message.

    Message Form
    message = message to be sent
    """

    # find recipient and user and get message to be sent
    user = User.query.filter_by(username=recipient).first()
    message = request.form["message"]

    if user == current_user:
        return WebHelpers.EasyResponse("You cannot send a message to yourself.", 400)

    if recipient is None:
        return WebHelpers.EasyResponse("User with that username does not exist.", 404)

    if message is None:
        return WebHelpers.EasyResponse("Can not send empty message.", 400)

    # create new message and write to db
    msg = Message(author=current_user, recipient=user, body=message)

    db.session.add(msg)
    db.session.commit()
    user.add_notification("unread_message_count", user.new_messages())
    db.session.commit()

    logging.debug(f"{current_user.name} sent message to {user.name}")

    return WebHelpers.EasyResponse(f"Message sent to {user.username}.", 201)


@message_bp.route("/api/notifications")
@login_required
def notifications():

    since = request.args.get("since", 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since
    ).order_by(Notification.timestamp.asc())

    return jsonify(
        [
            {"name": n.name, "data": n.get_data(), "timestamp": n.timestamp}
            for n in notifications
        ]
    )
