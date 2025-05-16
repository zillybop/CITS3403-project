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
    
    
    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id, accepted=True).first() is not None
    
    
    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now()) # "when image was stored" - from any source, e.g. tool/upload

    source_type = db.Column(db.String(64), default='uploaded')
    # 'uploaded' or 'tool-generated'
    tool_used = db.Column(db.String(64), nullable=True)
    parameters = db.Column(db.JSON, nullable=True) # For sobel, {'threshold':120}

    derived_from_id = db.Column(
        db.Integer,
        db.ForeignKey('image.id', name='fk_image_derived_from'),
        nullable=True
    )
    derived_from = db.relationship('Image', remote_side=[id])

    def __repr__(self):
        return (
            f"<Image id={self.id}, title='{self.title}', filename='{self.filename}', "
            f"user_id={self.user_id}, source_type='{self.source_type}', tool_used='{self.tool_used}', "
            f"derived_from_id={self.derived_from_id}>"
        )

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    source_type = db.Column(db.String(64), default='uploaded')  # 'uploaded', 'tool-generated', etc.
    
    image_id = db.Column(
        db.Integer,
        db.ForeignKey('image.id', name='fk_post_image'),
        nullable=True)
    image = db.relationship('Image', foreign_keys=[image_id], backref='posts')


    original_image_id = db.Column(
        db.Integer,
        db.ForeignKey('image.id', name='fk_post_original_image'),
        nullable=True)
    original_image = db.relationship('Image', foreign_keys=[original_image_id])
    # Possibly add comments and likes later.
    
    def is_derived_post(self):
        return self.source_type == 'tool-generated' and self.original_image is not None

    def __repr__(self):
        return (
            f"<Post id={self.id}, title='{self.title}', subtitle='{self.subtitle}', "
            f"user_id={self.user_id}, source_type='{self.source_type}', image_id={self.image_id}, "
            f"original_image_id={self.original_image_id}>"
        )
    
class FollowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<FollowRequest id={self.id} follower_id={self.follower_id} followed_id={self.followed_id} accepted={self.accepted}>"