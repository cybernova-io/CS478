from api.models.db import db
from datetime import datetime
from flask import current_app as app


class Message(db.Model):
    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)

    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "body": self.body,
            "timestamp": self.timestamp,
        }
