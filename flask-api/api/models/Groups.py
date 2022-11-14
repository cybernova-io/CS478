
"""
from api.models.db import db

group_user = db.Table(
    "group_users",
    db.Column("group_id", db.Integer, db.ForeignKey("Group.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("moderator", db.Integer)
)

class Group():
    __tablename__= "Group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
    owner = db.Column(db.Integer(), db.ForeignKey("Users.id"))
    members = db.relationship(
        "User",
        secondary=group_user,
        backref=db.backref("group_user", lazy="dynamic"),
    )
"""