from email.policy import default
from enum import unique
from api.models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine
from flask import current_app as app
from .Messages import Message
from .Notifications import Notification
import json
from .Posts import PostLike
from sqlalchemy import insert, values, select, update

# engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
#role = 1 = owner of group
#role = 2 = moderator of group
#role = 3 = member of group
group_user = db.Table(
    "group_users",
    db.Column("group_id", db.Integer, db.ForeignKey("Group.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("role", db.Integer)
)


blocked_user = db.Table(
    "blocked_users",
    db.Column("user_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("blocked_user_id", db.Integer, db.ForeignKey("Users.id")),
)

friend = db.Table(
    "friends",
    db.Column("friend0_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("friend1_id", db.Integer, db.ForeignKey("Users.id")),
)

pending_friend = db.Table(
    "pending_friends",
    db.Column("pending_friend0_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("pending_friend1_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("requestor", db.Integer),
)

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("Users.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("Role.id")),
)
class Group(db.Model):
    __tablename__= "Group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
    invite_only = db.Column(db.Boolean(), default=False, nullable=False)
    members = db.relationship("User", secondary=group_user, back_populates="groups", lazy="dynamic")
    posts = db.relationship("Post", backref="Posts", lazy="dynamic")

    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
            'description': self.description,
            'inviteOnly': self.invite_only 
        }

    def make_owner(self, user, current_user=None):
        if current_user != None:
            if self.check_role(user):
                if self.check_role(current_user) == 'Owner':
                    stmt = (
                    update(group_user).
                    where(group_user.c.user_id == user.id).
                    where(group_user.c.group_id == self.id).
                    values(role=1)
                )
                db.session.execute(stmt)    
                db.session.commit()
                stmt = (
                    update(group_user).
                    where(group_user.c.user_id == current_user.id).
                    where(group_user.c.group_id == self.id).
                    values(role=2)
                )
                db.session.execute(stmt)
                db.session.commit()
        else:
            stmt = insert(group_user).values(group_id=self.id, user_id=user.id, role=1)
            db.session.execute(stmt)
            db.session.commit()
            """
            stmt = (
                update(group_user).
                where(group_user.c.user_id == current_user.id).
                where(group_user.c.group_id == self.id).
                values(role=2)
            )
            db.session.execute(stmt)
            db.session.commit()
            """

    def make_moderator(self, user):
        if self.check_role(user):
            stmt = (
                update(group_user).
                where(group_user.c.user_id == user.id).
                where(group_user.c.group_id == self.id).
                values(role=2)
            )
            db.session.execute(stmt)
            db.session.commit()
        else:
            stmt = insert(group_user).values(group_id=self.id, user_id=user.id, role=2)
            db.session.execute(stmt)
            db.session.commit()
        

    def check_role(self, user):
        result = db.session.execute(group_user.select(group_user.c.role).where(group_user.c.group_id==self.id, group_user.c.user_id==user.id)).first()
        if result:
            if result[2] == 1:
                #print('Owner')
                return "Owner"
            elif result[2] == 2:
                #print('Moderator')
                return "Moderator"
            elif result[2] == 3:
                #print('Member')
                return "Member"
            else:
                return None
        else:
            #user is not in the group
            return None

class Role(db.Model):
    __tablename__ = "Role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model):
    """User account model."""

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False, unique=False)
    last_name = db.Column(db.String(25), nullable=False, unique=False)
    major = db.Column(db.String(30), nullable=False, unique=False)
    grad_year = db.Column(db.String(4), nullable=False, unique=False)
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    profile_pic = db.Column(db.String(), index=False, unique=False, nullable=True)
    friend_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    # feed = db.Column(db.Integer, db.ForeignKey('Feed.id'))
    active = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    current_login_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login_ip = db.Column(db.String())
    current_login_ip = db.Column(db.String())
    login_count = db.Column(db.Integer)
    groups = db.relationship("Group", secondary=group_user, back_populates="members", lazy="dynamic")
    
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    blocked_users = db.relationship(
        "User",
        secondary=blocked_user,
        primaryjoin=(blocked_user.c.user_id == id),
        secondaryjoin=(blocked_user.c.blocked_user_id == id),
        backref=db.backref("blocked_user", lazy="dynamic"),
        lazy="dynamic",
    )

    pending_friends = db.relationship(
        "User",
        secondary=pending_friend,
        primaryjoin=(pending_friend.c.pending_friend0_id == id),
        secondaryjoin=(pending_friend.c.pending_friend1_id == id),
        backref=db.backref("pending_friend", lazy="dynamic"),
        lazy="dynamic",
    )

    friends = db.relationship(
        "User",
        secondary=friend,
        primaryjoin=(friend.c.friend0_id == id),
        secondaryjoin=(friend.c.friend1_id == id),
        backref=db.backref("friend", lazy="dynamic"),
        lazy="dynamic",
    )

    messages_sent = db.relationship(
        "Message", foreign_keys="Message.sender_id", backref="author", lazy="dynamic"
    )

    posts = db.relationship("Post", backref="user", lazy="dynamic")

    messages_received = db.relationship(
        "Message",
        foreign_keys="Message.recipient_id",
        backref="recipient",
        lazy="dynamic",
    )

    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship("Notification", backref="user", lazy="dynamic")

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def set_creation_date(self):
        self.created_on = datetime.today()

    def set_last_login(self):
        self.last_login = datetime.today()
        db.session.commit()

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def add_friend(self, user):
        if not self.is_friend(user):
            engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
            self.pending_friends.append(user)
            db.session.commit()
            engine.execute(
                pending_friend.update()
                .where(pending_friend.c.pending_friend0_id == user.id)
                .values(requestor=1)
            )

        return self

    def remove_friend(self, user):
        if self.is_friend(user):
            self.friends.remove(user)
            return self

    def add_pending_friend(self, user):
        if not self.is_friend(user):
            self.friends.append(user)
            self.pending_friends.remove(user)
            return self

    def remove_pending_friend(self, user):
        if not self.is_friend(user):
            self.pending_friends.remove(user)
            return self

    def get_pending_friends(self):
        return [user.serialize() for user in pending_friend]

    def is_friend(self, user):
        return self.friends.filter(friend.c.friend1_id == user.id).count() > 0

    def is_requestor(self, friend):
        # Retrieves the value from db to see if current user is requestor, looking for 1 in requestor column
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        user_who_sent_request = engine.execute(
            pending_friend.select(pending_friend.c.requestor).where(
                pending_friend.c.pending_friend0_id == self.id,
                pending_friend.c.pending_friend1_id == friend.id,
            )
        ).fetchall()
        try:
            if user_who_sent_request[0][2] == 1:
                return True
            else:
                return False
        except IndexError as e:
            return False

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return (
            Message.query.filter_by(recipient=self)
            .filter(Message.timestamp > last_read_time)
            .count()
        )

    def is_blocked(self, user):
        return (
            self.blocked_users.filter(blocked_user.c.blocked_user_id == user.id).count()
            > 0
        )

    def add_blocked_user(self, user):
        if not self.is_blocked(user):
            stmt = insert(blocked_user).values(user_id=self.id, blocked_user_id=user.id)
            db.session.execute(stmt)
            db.session.commit()

            if self.is_friend(user):
                remove = self.remove_friend(user)
                db.session.add(remove)
                db.session.commit()

            if user.id in self.pending_friends:
                removed = self.remove_pending_friend
                db.session.add(removed)
                db.session.commit()

    def remove_blocked_user(self, user):
        if self.is_blocked(user):
            stmt = (
                blocked_user.delete()
                .where(blocked_user.c.user_id == self.id)
                .where(blocked_user.c.blocked_user_id == user.id)
            )

            db.session.execute(stmt)
            db.session.commit()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def in_group(self, group):
        return (
            self.groups.filter(group_user.c.group_id == group.id).count()
            > 0
        )

    def join_group(self, group):
        if not self.in_group(group):
            stmt = insert(group_user).values(user_id=self.id, group_id=group.id, role=3)
            db.session.execute(stmt)
            db.session.commit()

    def leave_group(self, group):
        if self.in_group(group):
            stmt = (
                    group_user.delete()
                    .where(group_user.c.user_id == self.id)
                    .where(group_user.c.group_id == group.id)
                )
            db.session.execute(stmt)
            db.session.commit()

    def is_admin(self):
        if 'Admin' in [x.name for x in self.roles]:
            return True
        else:
            return False


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name
        }

    def serialize_search(self):
        return {
            "id": self.id,
            "username": self.username,
            "major": self.major,
            "gradYear": self.grad_year,
        }

    def serialize_id(self):
        return {"id": self.id}
