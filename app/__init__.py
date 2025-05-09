from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager



db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'introductory' # TODO Where to redirect if not logged in
login_manager.login_message = "You must be logged in to use this feature."
login_manager.login_message_category = 'warning'

from app import routes, models
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------ Temporary Admin Account ------------
from werkzeug.security import generate_password_hash
with app.app_context():
    if not User.query.filter_by(username='admin').first():
        user = User(username="admin", password_hash=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()