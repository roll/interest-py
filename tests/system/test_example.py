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

    def test(self):
        response = self.server.make_request('GET', '/api/v1/comment/7')
        self.assertEqual(
            response.headers['CONTENT-TYPE'],
            'application/json; charset=utf-8')
        self.assertEqual(response.json, {'id': '7'})
