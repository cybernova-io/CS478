# from .. import db

# class Feed(db.Model):
#   __tablename__ = "Feed"

#  id = db.Column(db.Integer, primary_key=True)
# owner = db.Column(db.Integer, db.relationship('User.feed'), backref='owner', lazy=True)
# friend_post = db.Column(db.Integer, db.relationship('Post.id', backref='friend_post', lazy='dynamic'))

# def serialize(self):
#   return{
#      "id": self.id,
#     "owner": self.owner,
#    "friend_post": self.friend_post,

# }
