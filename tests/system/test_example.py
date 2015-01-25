import unittest
from tests.system.server import Server


class ExampleTest(unittest.TestCase):

    # Actions

    @classmethod
    def setUpClass(cls):
        cls.server = Server('demo/example.py')
        cls.server.listen()

    @classmethod
    def tearDownClass(cls):
        cls.server.close()

    # Tests

    def test_read(self):
        response = self.server.make_request('GET', '/api/v1/comment/7')
        self.assertEqual(response.status, 200)
        self.assertEqual(
            response.headers['CONTENT-TYPE'],
            'application/json; charset=utf-8')
        self.assertEqual(response.json, {'key': 7})

    def test_upsert(self):
        response = self.server.make_request('PUT', '/api/v1/comment')
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json, {'message': 'Created'})

    def test_not_found(self):
        response = self.server.make_request('PUT', '/api/v1/not-found')
        self.assertEqual(response.status, 404)
