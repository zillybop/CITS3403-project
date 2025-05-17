"""Test package for the Flask app."""
import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import User
import os, shutil
import io

class BaseTestCase(unittest.TestCase):
    def create_user(self, username='testuser', password='password'):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def create_and_login_user(self, username='testuser', password='password'):
        user = self.create_user(username, password)
        self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)
        return user

    def upload_image(self, title='Test Image', filename='test.png', content=b'fakeimg'):
        data = {
            'title': title,
            'image': (io.BytesIO(content), filename)
        }
        return self.client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

    def upload_processed_image(self, tool='sobel', threshold=100):
        self.upload_image()
        from app.models import Image
        image = Image.query.first()
        image.tool_used = tool
        image.parameters = {'threshold': threshold}
        db.session.commit()
        return image

    def setUp(self):
        self.app = create_app(TestConfig)
        print(f"[TEST] Upload folder: {self.app.config['UPLOAD_FOLDER']}")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

        # Clean mkdtemp file
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'], ignore_errors=True)

