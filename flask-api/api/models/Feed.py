from .. import db

class Feed(db.Model):
    """Model for the feed."""

    __tablename__ = "Feed"

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.relationship('User.feed'), backref='owner', lazy=True)



    


