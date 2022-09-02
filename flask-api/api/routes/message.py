from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory, jsonify, Response
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

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/api/messages')
@login_required
def messages():

    if request.method == 'GET':

        current_user.last_message_read_time = datetime.utcnow()
        current_user.add_notification('unread_message_count', 0)
        db.session.commit()

        data = {}
        counter = 1

        # support for pagination, i.e. only display 10 messages per page
        page = request.args.get('page', 1, type=int)

        messages = current_user.messages_received.order_by(
            Message.timestamp.desc()).paginate(
                page, app.config['MESSAGES_PER_PAGE'], False)
            
        next_url = url_for('message_bp.messages', page=messages.next_num) \
            if messages.has_next else None
        prev_url = url_for('message_bp.messages', page=messages.prev_num) \
            if messages.has_prev else None

        for i in messages.items:
            data[f'message_{counter}'] = i.serialize()

        data['next_url'] = next_url
        data['prev_ul'] = prev_url
        
        resp = jsonify(data)
        resp.status_code = 200

        return resp
    else:
        return WebHelpers.EasyResponse('GET method should be used for retrieving messages.', 405)
    

@message_bp.route('/api/send-message/<recipient>', methods=['GET', 'POST'])
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
    user = User.query.filter_by(name=recipient).first()
    message = request.form['message']
    
    if recipient is None:
        return WebHelpers.EasyResponse('User with that name does not exist.', 404)

    if message is None:
        return WebHelpers.EasyResponse('Can not send empty message.', 400)
    
    #create new message and write to db
    msg = Message(author=current_user,
                 recipient=user,
                body=message)

    db.session.add(msg)
    db.session.commit()
    user.add_notification('unread_message_count', user.new_messages())
    db.session.commit()

    logging.debug(f'{current_user.name} sent message to {user.name}')

    return WebHelpers.EasyResponse('Message sent.', 201)

@message_bp.route('/api/notifications')
@login_required
def notifications():

    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())

    return jsonify([{'name': n.name,'data': n.get_data(),'timestamp': n.timestamp} for n in notifications])
