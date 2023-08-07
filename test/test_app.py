import unittest
from app import app, sanitize_column_name
import io

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_upload_csv(self):
        data = {
            'file': (io.BytesIO(b'header1,header2\nvalue1,value2'), 'test.csv'),
        }
        response = self.client.post('/upload?table=test_table', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('File contents saved to table test_table', response.get_data(as_text=True))

    def test_upload_without_csv(self):
        response = self.client.post('/upload?table=test_table')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file part in the request', response.get_data(as_text=True))

    def test_upload_non_csv_file(self):
        data = {
            'file': (io.BytesIO(b'some content'), 'test.txt'),
        }
        response = self.client.post('/upload?table=test_table', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid file type, please upload a CSV file', response.get_data(as_text=True))

    def test_sanitize_column_name(self):
        self.assertEqual(sanitize_column_name("Header"), "Header")
        self.assertEqual(sanitize_column_name("Test Header"), "Test_Header")
        self.assertEqual(sanitize_column_name("  Test Header  "), "__Test_Header__")
        self.assertEqual(sanitize_column_name("1Test"), "_1Test")

if __name__ == '__main__':
    unittest.main()