from app import app
import unittest

class MyTests(unittest.TestCase):
    
    def test_page(self):
        c = app.test_client()
        res = c.get('/')
        self.assertEqual(res.status_code, 200)

    def test_post(self):
        c = app.test_client()
        res = c.post('/generate', data={"text": "hello this is a test line for flask app"})
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()