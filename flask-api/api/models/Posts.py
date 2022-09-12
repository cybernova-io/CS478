from datetime import datetime
from os import abort
from flask import Blueprint, redirect, render_template, flash, request, session, url_for, jsonify, Response
from flask_login import login_required, logout_user, current_user, login_user
from .. import db
from .. import login_manager
from flask_login import logout_user
import werkzeug
import os
from flask import current_app as app
from sqlalchemy import engine, create_engine
import logging

post_bp = Blueprint('post_bp', __name__)


class Post(db.Model):
    """Posts model."""
    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    author = db.Column(db.Integer, db.ForeignKey('Users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    likes = db.relationship('PostLike', backref='Posts')
    # backref adds a new column on the child (child being PostLike))

class PostLike(db.Model):
    __tablename__= 'post_like'


    id = db.Column(db.Integer, primary_key=True)
    # put FK on the child 
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))



liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='Users', lazy='dynamic')

def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=Post.id)
            db.session.add(like)  

def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=Post.id).delete()

def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == Post.id).count() > 0
