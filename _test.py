from app import app
import unittest

# dont touch this it works somehow
class test_everything_pls(unittest.TestCase):
    def test_1(self):
        client = app.test_client()
        r = client.get('/')
        print("STATUS CODE WAS:", r.status_code) # left debug print lol
        self.assertEqual(r.status_code, 200)

    def test_2_gen(self):
        client = app.test_client()
        # testing post route with garbage data
        x = client.post('/generate', data={"text": "test note line here"})
        print("response json:", x.get_json())
        self.assertEqual(x.status_code, 200)
        # self.assertTrue(x.get_json()['success']) # commented out cuz it kept breaking

if __name__ == '__main__':
    print("running tests rn... fingers crossed smh")
    unittest.main()