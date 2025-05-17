import io
from app.models import Image, FollowRequest
from app.tests.__init__ import BaseTestCase
from app import db

class FeedAccessTest(BaseTestCase):
    def test_social_feed_requires_login(self):
        response = self.client.get('/social/feed')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/introductory', response.headers['Location'])


class SocialTests(BaseTestCase):
    def test_create_post_success(self):
        self.create_and_login_user()
        self.upload_image(title='test', filename='img.png', content=b'data')
        img_id = Image.query.first().id
        response = self.client.post('/social/post/create', data={
            'title': 'Post 1',
            'subtitle': 'Intro',
            'image_id': img_id
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'post', response.data.lower())

    def test_list_users_page(self):
        self.create_and_login_user()
        response = self.client.get('/social/users')
        self.assertEqual(response.status_code, 200)

    def test_send_follow_request(self):
        self.create_user(username='bob')
        self.create_and_login_user(username='alice')
        response = self.client.post('/follow/bob', follow_redirects=True)
        self.assertIn(b'request', response.data.lower())

    def test_remove_nonexistent_follower(self):
        self.create_and_login_user()
        response = self.client.post('/social/remove_follower/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_social_inbox_access(self):
        self.create_and_login_user()
        response = self.client.get('/social/inbox')
        self.assertEqual(response.status_code, 200)

    def test_accept_follow_request_invalid(self):
        self.create_and_login_user()
        response = self.client.post('/social/accept_follow/1234', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_send_follow_request_success(self):
        bob = self.create_user('bob')
        alice = self.create_and_login_user('alice')

        self.client.post(f'/social/follow/{bob.id}', follow_redirects=True)

        fr = FollowRequest.query.filter_by(follower_id=alice.id, followed_id=bob.id).first()
        self.assertIsNotNone(fr)
        self.assertFalse(fr.accepted)

    def test_remove_follower_success(self):
        alice = self.create_user('alice')
        bob = self.create_and_login_user('bob')
        # simulate accepted follow
        fr = FollowRequest(followed_id=bob.id, follower_id=alice.id, accepted=True)
        db.session.add(fr)
        db.session.commit()
        response = self.client.post(f'/social/remove_follower/{alice.id}', follow_redirects=True)
        self.assertIn(b'removed', response.data.lower())