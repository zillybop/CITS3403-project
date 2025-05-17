from app.tests import BaseTestCase

class ApiTests(BaseTestCase):
    def test_api_user_search(self):
        self.create_user(username='alice', password='a')
        self.create_and_login_user(username='bob', password='b')

        response = self.client.get('/api/users/search?q=ali')
        self.assertIn(b'alice', response.data)

    def test_api_search_multiple_users(self):
        self.create_user(username='alice', password='a')
        self.create_user(username='bob', password='b')
        self.create_user(username='charlie', password='c')
        self.create_and_login_user(username='david', password='d')

        response = self.client.get('/api/users/search?q=a')
        self.assertIn(b'alice', response.data)
        self.assertNotIn(b'bob', response.data)

    def test_api_search_no_match(self):
        self.create_user(username='eve', password='e')
        self.create_and_login_user(username='frank', password='f')

        response = self.client.get('/api/users/search?q=xyz')
        self.assertNotIn(b'eve', response.data)
        self.assertEqual(response.status_code, 200)

    def test_api_search_after_follow(self):
        alice = self.create_user(username='alice', password='a')
        self.create_and_login_user(username='bob', password='b')

        self.client.post(f'/follow/{alice.username}', follow_redirects=True)
        response = self.client.get('/api/users/search?q=ali')
        self.assertIn(b'alice', response.data)