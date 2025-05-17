"""Test package for the Flask app."""
import unittest
from app import create_app, db
from app.config import TestConfig
from models import User

class BaseTestCase(unittest.TestCase):
    def create_user(self, username='testuser', password='password'):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

