from api.models.db import db
from datetime import datetime


event_attendees = db.Table(
    "event_attendees",
    db.Column("user_id", db.Integer(), db.ForeignKey("Users.id")),
    db.Column("event_id", db.Integer(), db.ForeignKey("Events.id")),
)


class Event(db.Model):
    __tablename__ = "Events"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    description = db.Column(db.String())
    name = db.Column(db.String())
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    attendees = db.relationship(
        "User", secondary=event_attendees, backref=db.backref("event", lazy="dynamic")
    )

    def in_event(self, user):
        if user in self.attendees:
            return True

    def join_event(self, user):
        if not self.in_event(user):
            self.attendees.append(user)
            db.session.commit()
            return self

    def leave_event(self, user):
        if self.in_event(user):
            self.attendees.remove(user)
            db.session.commit()
            return self

    def serialize(self):
        return {
            "id": self.id,
            "event_owner": self.owner_id,
            "event_name": self.name,
            "event_description": self.description,
            "event_scheduled_time": self.time,
            "event_attendes": [x.serialize() for x in self.attendees],
        }
