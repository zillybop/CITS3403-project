import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback-dev-key"
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.db')

class TestConfig(Config):
    TESTING = True 
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    UPLOAD_FOLDER = tempfile.mkdtemp()