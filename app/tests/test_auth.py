from app.tests.__init__ import BaseTestCase
from flask_login import current_user

class AuthTests(BaseTestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_introductory(self):
        response = self.client.get('/introductory')
        self.assertEqual(response.status_code, 200)

    def test_register_then_login_logout(self):
        self.client.post('/register', data={'username': 'u', 'password': 'p', 'password2': 'p'}, follow_redirects=True)
        self.client.get('/logout', follow_redirects=True)
        response = self.client.post('/login', data={'username': 'u', 'password': 'p'}, follow_redirects=True)
        self.assertIn(b'Logged in successfully', response.data)

    def test_logout_redirects_to_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You must be logged in', response.data)

class RegistrationTests(BaseTestCase):
    def test_register_with_valid_data(self):
        with self.client:
            response = self.client.post('/register', data={
                'username': 'alice',
                'password': 'securepass',
                'password2': 'securepass'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'alice')

    def test_register_missing_fields(self):
        response = self.client.post('/register', data={'username': '', 'password': 'pw', 'password2': 'pw'}, follow_redirects=True)
        self.assertIn(b'required', response.data.lower())

    def test_register_password_mismatch(self):
        response = self.client.post('/register', data={'username': 'u1', 'password': 'a', 'password2': 'b'}, follow_redirects=True)
        self.assertIn(b'match', response.data.lower())

    def test_register_existing_user(self):
        self.client.post('/register', data={'username': 'dup', 'password': 'pw', 'password2': 'pw'}, follow_redirects=True)
        response = self.client.post('/register', data={'username': 'dup', 'password': 'pw', 'password2': 'pw'}, follow_redirects=True)
        self.assertIn(b'already exists', response.data.lower())

class LoginTests(BaseTestCase):
    def test_login_invalid_credentials(self):
        response = self.client.post('/login', data={
            'username': 'invaliduser',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_missing_fields(self):
        response = self.client.post('/login', data={'username': '', 'password': ''}, follow_redirects=True)
        self.assertIn(b'required', response.data.lower())

    def test_login_invalid_credentials(self):
        response = self.client.post('/login', data={'username': 'nope', 'password': 'wrong'}, follow_redirects=True)
        self.assertIn(b'invalid', response.data.lower())