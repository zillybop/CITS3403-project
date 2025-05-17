from app.tests import BaseTestCase
from app.models import Image, Post

class PostTests(BaseTestCase):
    def test_create_post_success(self):
        self.create_and_login_user()
        self.upload_image(title='TestImage', filename='test.png', content=b'img')
        image = Image.query.first()
        response = self.client.post('/social/post/create', data={
            'title': 'My Post',
            'subtitle': 'Intro subtitle',
            'image_id': image.id
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post created successfully', response.data) # From flash message

        post = Post.query.filter_by(title='My Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.subtitle, 'Intro subtitle')