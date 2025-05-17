from app.tests import BaseTestCase

class ToolTests(BaseTestCase):
    def test_save_photo_requires_login(self):
        response = self.client.post('/social/feed/save_photo/1', data={}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_reopen_tool_invalid_image_id(self):
        self.create_and_login_user()
        response = self.client.get('/social/feed/reopen_tool/400', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'image not found.', response.data.lower())

    def test_edge_detect_invalid_image_data(self):
        self.create_and_login_user()
        response = self.client.post('/tools/edge_detect', data={
            'tool': 'sobel',
            'threshold': 100,
            'input_image_id': 1,
            'output_image_dataurl': 'not-an-image'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'invalid image data', response.data.lower())
    
    def test_visualise_page_loads(self):
        self.create_and_login_user()
        response = self.client.get('/tools/visualise')
        self.assertEqual(response.status_code, 200)

    def test_histogram_page_loads(self):
        self.create_and_login_user()
        response = self.client.get('/tools/histogram')
        self.assertEqual(response.status_code, 200)

    def test_edge_detect_prefill_render(self):
        self.create_and_login_user()
        img = self.upload_processed_image()
        response = self.client.get(f'/tools/edge_detect?image_id={img.id}&tool=sobel&threshold=120')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'select one of your uploaded images', response.data.lower())