"""Database models."""
from email.policy import default
from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine
from flask import current_app as app

like = db.Table('likes',
    db.Column('like0_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('like1_id ', db.Integer, db.ForeignKey('Users.id'))
)

class Post(db.Model):
    """Posts model."""

    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(), unique=False, nullable=False)
    #owner_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    
class Comment(db.Model):
    """
    Comments Model.
    """
   
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)

"""
class Likes(db.Model):
    
    Likes Model.
    
    __tablename__= 'Likes'
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
"""
   
