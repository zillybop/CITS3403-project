def test_api_user_search(self):
    self.login()
    self.client.post('/register', data={'username': 'alice', 'password': 'a', 'password2': 'a'})
    response = self.client.get('/api/users/search?q=ali')
    self.assertIn(b'alice', response.data)