from app.tests.__init__ import BaseTestCase
import io

class UploadAccessTest(BaseTestCase):
    def test_upload_requires_login(self):
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/introductory', response.headers['Location'])

def test_upload_get_renders_form(self):
    self.login()
    response = self.client.get('/upload')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Image File', response.data)

def test_upload_post_valid_image(self):
    self.login()
    image_data = (io.BytesIO(b'test'), 'test.png')
    response = self.client.post('/upload', data={
        'title': 'Test',
        'image': image_data
    }, content_type='multipart/form-data', follow_redirects=True)
    self.assertIn(b'Upload successful', response.data)

def test_uploaded_file_serves(self):
    self.login()
    # Upload an image first
    image_data = (io.BytesIO(b'test'), 'file.png')
    self.client.post('/upload', data={
        'title': 'Test',
        'image': image_data
    }, content_type='multipart/form-data')
    response = self.client.get('/uploads/file.png')
    self.assertEqual(response.status_code, 200)