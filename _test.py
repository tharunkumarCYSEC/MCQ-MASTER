
from app import app
import unittest

class SimpleAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    def test_generate(self):
        res = self.app.post('/generate', json={"text": "Flask is lightweight."})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()