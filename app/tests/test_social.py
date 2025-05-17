from app.tests.__init__ import BaseTestCase

class FeedAccessTest(BaseTestCase):
    def test_social_feed_requires_login(self):
        response = self.client.get('/social/feed')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/introductory', response.headers['Location'])


def test_create_post_success(self):
    self.login()
    # Upload image first to get ID
    image_data = (io.BytesIO(b'data'), 'img.png')
    self.client.post('/upload', data={'title': 'test', 'image': image_data}, content_type='multipart/form-data')
    img_id = Image.query.first().id
    response = self.client.post('/post/create', data={
        'title': 'Post 1',
        'subtitle': 'Intro',
        'image_id': img_id
    }, follow_redirects=True)
    self.assertIn(b'created', response.data.lower())