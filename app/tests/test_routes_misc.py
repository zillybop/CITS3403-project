from app.tests.__init__ import BaseTestCase
from app.models import Image, FollowRequest
from app import db

class MiscTests(BaseTestCase):
    def test_save_own_photo(self):
        self.create_and_login_user()
        img = self.upload_processed_image()
        response = self.client.post(f'/social/feed/save_photo/{img.id}', data={
            'tool': 'sobel',
            'threshold': 100,
            'input_image_id': img.id,
            'output_image_dataurl': 'data:image/png;base64,iVBORw0KGgoAAAANS...'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'this image is already in your uploads.', response.data.lower())

    def test_save_photo_success(self):
        alice = self.create_user('alice', 'a')
        self.client.post('/login', data={'username': 'alice', 'password': 'a'}, follow_redirects=True)
        self.upload_processed_image()
        from app.models import Post
        img = Image.query.first()
        post = Post(
            title="shared image",
            subtitle="demo post",
            user_id=alice.id,
            image=img,
            source_type="uploaded"
        )
        db.session.add(post)
        db.session.commit()
        self.client.get('/logout', follow_redirects=True)

        bob = self.create_and_login_user('bob', 'b')
        fr = FollowRequest(followed_id=alice.id, follower_id=bob.id, accepted=True)
        db.session.add(fr)
        db.session.commit()
        img = Image.query.first()
        response = self.client.post(f'/social/feed/save_photo/{img.id}', data={
            'tool': 'sobel',
            'threshold': 100,
            'input_image_id': img.id,
            'output_image_dataurl': 'data:image/png;base64,iVBORw0KGgoAAAANS...'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'image added to your uploads!', response.data.lower())