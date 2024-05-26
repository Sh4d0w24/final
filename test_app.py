import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import unittest
import json
from app import app
from base64 import b64encode

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_product(self):
        token = self.get_token()
        response = self.app.post('/product', data=json.dumps(dict(name='Product21', description='New Product', price=19.99)), content_type='application/json', query_string={'token': token})
        self.assertEqual(response.status_code, 201)

    def test_get_product(self):
        response = self.app.get('/product/1')
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        token = self.get_token()
        response = self.app.put('/product/1', data=json.dumps(dict(name='Updated Product', description='Updated description', price=29.99)), content_type='application/json', query_string={'token': token})
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        token = self.get_token()
        response = self.app.delete('/product/21', query_string={'token': token})
        self.assertEqual(response.status_code, 200)

    def test_search_products(self):
        response = self.app.get('/products', query_string={'name': 'Product1'})
        self.assertEqual(response.status_code, 200)

    def get_token(self):
        response = self.app.post('/login', headers={'Authorization': 'Basic ' + b64encode(b"admin:password").decode('utf-8')})
        return json.loads(response.data)['token']

if __name__ == '__main__':
    unittest.main()
