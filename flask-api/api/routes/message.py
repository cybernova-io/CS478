from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect
)
from flask_jwt_extended import jwt_required, current_user
from ..models.Users import db, User, pending_friend, Message
from datetime import datetime
from ..services.WebHelpers import WebHelpers
import logging
from ..models.Notifications import Notification
from .message import Message

message_bp = Blueprint("message_bp", __name__)

@message_bp.get("/messages")
@jwt_required()
def messages_page():
    messages = Message.query.filter(
        (Message.sender_id == current_user.id)
        | (Message.recipient_id == current_user.id)
    ).all()
    conversations = []
    for message in messages:
        if message.sender_id != current_user.id:
            conversations.append(message.sender_id)
        if message.recipient_id != current_user.id:
            conversations.append(message.recipient_id)
    
    conversations = set(conversations)

    users = []
    for i in conversations:
        users.append(User.query.get(i).serialize())
    

    return render_template("/messages/messages.html", users=users)

@message_bp.route("/messages/conversation/<int:id>", methods = ['GET', 'POST'])
@jwt_required()
def conversations_page(id):

    if request.method == 'GET':
        messages = Message.query.filter((Message.sender_id == id) | (Message.recipient_id == id)).filter((Message.sender_id == current_user.id) | (Message.recipient_id == current_user.id)).all()

        user = User.query.get(id).serialize()
        cur_user = current_user.serialize()

        for i in messages:
            if i.sender_id == id:
                i.user = user
            else:
                i.user = cur_user

        return render_template("/messages/conversation.html", messages=messages, conv=user)

@message_bp.post("/messages/delete/<int:id>/<int:convId>")
@jwt_required()
def delete_message_page(id, convId):

    message = Message.query.get(id)

    if message.sender_id == current_user.id or current_user.is_admin():
        db.session.delete(message)
        db.session.commit()
        return redirect(f'/messages/conversation/{convId}')

@message_bp.post("/messages/send/<int:id>")
@jwt_required()
def send_message_page(id):

    text = request.form.get("msg")

    message = Message(
        sender_id=current_user.id,
        recipient_id=id,
        body=text
    )
    db.session.add(message)
    db.session.commit()

    return redirect(f'/messages/conversation/{id}')
    


######################################################### API BELOW, SERVER RENDERING ABOVE

@message_bp.get("/api/messages")
@jwt_required()
def messages():
    messages = Message.query.filter(
        (Message.sender_id == current_user.id)
        | (Message.recipient_id == current_user.id)
    ).all()

    data = jsonify([x.serialize() for x in messages])

    resp = data
    resp.status_code
    return data


@message_bp.get("/api/messages/<string:user>")
@jwt_required()
def messages_user(user):

    current_user.last_message_read_time = datetime.utcnow()
    # current_user.add_notification("unread_message_count", 0)
    db.session.commit()

    data = {}

    friend = User.query.filter_by(username=user).first()

    if friend is None:
        return WebHelpers.EasyResponse("Specified user does not exist.", 404)
    messages = (
        Message.query.order_by(Message.timestamp.asc())
        .filter(
            (Message.recipient_id == friend.id) | (Message.sender_id == current_user.id)
        )
        .all()
    )

    # messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, app.config['MESSAGES_PER_PAGE'], False )
    # messages = current_user.messages_received.where(
    #    Message.sender_id == friend.id
    # ).all()

    if messages is None:
        return WebHelpers.EasyResponse("You have no messages with this user.", 400)

    data = [x.serialize() for x in messages]

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@message_bp.post("/api/send-message/<recipient>")
@jwt_required()
def send_message(recipient):
    """
    Allows user to send a private message to another user.
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
    # user.add_notification("unread_message_count", user.new_messages())
    db.session.commit()

    logging.debug(f"{current_user.username} sent message to {user.username}")

    return WebHelpers.EasyResponse(f"Message sent to {user.username}.", 201)


@message_bp.route("/api/notifications")
@jwt_required()
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
