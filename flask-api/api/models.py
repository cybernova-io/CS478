"""Database models."""
from email.policy import default
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine
from flask import current_app as app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

friend = db.Table('friends',
    db.Column('friend0_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('friend1_id', db.Integer, db.ForeignKey('Users.id'))
)

pending_friend = db.Table('pending_friends',
    db.Column('pending_friend0_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('pending_friend1_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('requestor', db.Integer)
)

comments = db.Table('comments',
    db.Column('comment_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('comment_author', db.String(), db.ForeignKey('Users.id'))
)
likes = db.Table('likes',
    db.Column('like_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('like_author', db.String(), db.ForeignKey('Users.id'))
)

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False,nullable=True)



    likes = db.relationship('Likes', db.relationship('User', 
                               backref=db.backref('likes', lazy='dynamic'),
                               lazy='dynamic'))


    profile_pic = db.Column(db.String(), index=False, unique=False, nullable=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    
    pending_friends = db.relationship('User', 
                               secondary=pending_friend, 
                               primaryjoin=(pending_friend.c.pending_friend0_id == id), 
                               secondaryjoin=(pending_friend.c.pending_friend1_id == id), 
                               backref=db.backref('pending_friend', lazy='dynamic'),
                               lazy='dynamic')

    friends = db.relationship('User', 
                               secondary=friend, 
                               primaryjoin=(friend.c.friend0_id == id), 
                               secondaryjoin=(friend.c.friend1_id == id), 
                               backref=db.backref('friend', lazy='dynamic'), 
                               lazy='dynamic')
    
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def set_creation_date(self):
        self.created_on = datetime.today()

    def set_last_login(self):
        self.last_login = datetime.today()
        db.session.commit()

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def add_friend(self, user):
        if not self.is_friend(user):
            self.pending_friends.append(user)
            db.session.commit()
            engine.execute(pending_friend.update().where(
                pending_friend.c.pending_friend0_id == user.id).values(requestor=1))
            
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
        #Retrieves the value from db to see if current user is requestor, looking for 1 in requestor column
        user_who_sent_request = engine.execute(pending_friend.select(pending_friend.c.requestor).where(
                                    pending_friend.c.pending_friend0_id == self.id, pending_friend.c.pending_friend1_id == friend.id)).fetchall()
        try:
            if user_who_sent_request[0][2] == 1:
                return True
            else:
                return False
        except IndexError as e:
            return False


    def serialize(self):
        return {
            'user_id': self.id,
            'user_name': self.name,
        }

class Post(db.Model):
    """Posts model."""

    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Likes', backref='post', passive_deletes=True)



"""
class Comment(db.Model):
   
   __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)   
class Likes(db.Model):
    
    __tablename__= 'Likes'
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

"""

 