# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the payment test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.payment = {'commonid': 'online'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_payment_creation(self):
        """Test API can create a payment (POST request)"""
        res = self.client().post('/api/payments/', data=self.payment)
        self.assertEqual(res.status_code, 201)
        self.assertIn('online', str(res.data))

    def test_api_can_get_all_payments(self):
        """Test API can get a payment (GET request)."""
        res = self.client().post('/api/payments/', data=self.payment)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/payments/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('online', str(res.data))

    def test_api_can_get_payment_by_id(self):
        """Test API can get a single payment by using it's id."""
        rv = self.client().post('/api/payments/', data=self.payment)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/payments/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('online', str(result.data))

    def test_payment_can_be_edited(self):
        """Test API can edit an existing payment. (PUT request)"""
        rv = self.client().post(
            '/api/payments/',
            data={'commonid': 'onlinepaybill'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/api/payments/1',
            data={
                "commonid": "online"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/api/payments/1')
        self.assertIn('onlinepay', str(results.data))

    def test_payment_deletion(self):
        """Test API can delete an existing payment. (DELETE request)."""
        rv = self.client().post(
            '/api/payments/',
            data={'commonid': 'onlinepaybill'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/api/payments/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/payments/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
