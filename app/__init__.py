from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager
from app.models import db
from flask_wtf.csrf import CSRFProtect, generate_csrf

csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
csrf.init_app(app)
app.jinja_env.globals['csrf_token'] = generate_csrf
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'introductory'
login_manager.login_message = "You must be logged in to use this feature."
login_manager.login_message_category = 'warning'

from app import routes, models
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))