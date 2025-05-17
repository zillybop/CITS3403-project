def test_save_photo_requires_login(self):
    response = self.client.post('/save_photo', data={}, follow_redirects=False)
    self.assertEqual(response.status_code, 302)