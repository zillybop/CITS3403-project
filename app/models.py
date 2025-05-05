from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    images = db.relationship('Image', backref='user', lazy=True)
    posts = db.relationship('Post', backref='user', lazy=True)

    followers = db.relationship(
        'FollowRequest',
        foreign_keys='FollowRequest.followed_id',
        backref='followed',
        lazy='dynamic'
    )

    following = db.relationship(
        'FollowRequest',
        foreign_keys='FollowRequest.follower_id',
        backref='follower',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id, accepted=True).first() is not None
    
    
    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Image id={self.id} filename={self.filename} title={self.title} user_id={self.user_id}>"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    image = db.relationship('Image')
    # Possibly add comments and likes later.

    def __repr__(self):
        return f"<Post id={self.id} title={self.title} user_id={self.user_id}>"
    
class FollowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<FollowRequest id={self.id} follower_id={self.follower_id} followed_id={self.followed_id} accepted={self.accepted}>"
    