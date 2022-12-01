from datetime import datetime
from os import abort
from flask import Blueprint
from flask_login import login_required, logout_user, current_user, login_user
from api.models.db import db
from flask_login import logout_user
from flask import current_app as app
from sqlalchemy import engine, create_engine
import logging


post_bp = Blueprint("post_bp", __name__)

liked = db.relationship(
    "PostLike", db.ForeignKey("PostLike.user_id"), backref="user", lazy="dynamic"
)
commented = db.relationship(
    "PostComment", db.ForeignKey("PostComment.user_id"), backref="user", lazy="dynamic"
)

user_comment = db.Table(
    "user_comments",
    db.Column("user_comment_id", db.Integer, db.ForeignKey("post_comment.id")),
    db.Column("user_comment_response_id", db.Integer, db.ForeignKey("post_comment.id")),
)

class Post(db.Model):
    """Posts model."""

    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    group_id = db.Column(db.Integer, db.ForeignKey('Group.id'), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    likes = db.relationship("PostLike", backref="Posts", lazy="dynamic")
    comments = db.relationship("PostComment", backref="Posts", lazy="dynamic")
    
    # feed = db.relationship("Users", backref="Posts", lazy="dynamic")

    def serialize(self):

        return {
            "id": self.id,
            "title": self.title,
            "text": self.content,
            "likes": [x.serialize() for x in self.likes],
            "comments": [x.serialize() for x in self.comments],
            #"comment_responses": [x.serialize() for x in self.comments.replies],
            "createdAt": self.date_created,
            "userId": self.user_id
        }

    def serialize_search(self):
        return {"id": self.id, "title": self.title, "text": self.content}


class PostLike(db.Model):
    __tablename__ = "post_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("Posts.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("Group.id"))

    def like_post(self, post, user):
        if not self.has_liked_post(post):
            like = PostLike(user_id=user.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return (
            PostLike.query.filter(
                PostLike.user_id == self.id, PostLike.post_id == post.id
            ).count()
            > 0
        )

    def serialize(self):
        return {"userId": self.user_id}


class PostComment(db.Model):
    _N = 6

    __tablename__ = "post_comment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("Posts.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("Group.id"))
    text = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    # for a reply, path is set to the path of the parent with the counter appended at the end
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'))

    replies = db.relationship(
        'PostComment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')


    """
    comment_replies = db.relationship(
        "PostComment",
        secondary=user_comment,
        primaryjoin=(user_comment.c.user_comment_id == id),
        secondaryjoin=(user_comment.c.user_comment_response_id == id),
        backref=db.backref("user_comment", lazy="dynamic"),
        remote_side=[id],
        lazy="dynamic")
    """
    
    
    def comment_post(self, user, post):
        if not self.has_commented_post(post):
            comment = PostComment(user_id=user.id, post_id=post.id)
            db.session.add(comment)

    def delete_comment(self, post):
        if self.has_commented_post(post):
            PostComment.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_commented_post(self, post):
        return (
            PostComment.query.filter(
                PostComment.user_id == self.id, PostComment.post_id == post.id
            ).count()
            > 0
        )

    def comment_reply(self, text):
        return PostComment(text=text, user_comment=self)

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.user_comment.path + '.' if self.user_comment else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        db.session.commit()

    # returns the indentation lvl of any given comment
    def level(self):
        return len(self.path) // self._N - 1

    def serialize(self):
        return {"id": self.id, 
                "userId": self.user_id, 
                "text": self.text,
                "createdAt": self.timestamp
            }

   

    

