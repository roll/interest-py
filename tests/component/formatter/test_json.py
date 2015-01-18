import unittest
from unittest.mock import patch
from importlib import import_module
component = import_module('interest.formatter.json')


class ClassTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.json = patch.object(component, 'json').start()
        self.formatter = component.JSONFormatter('service')

    # Tests

    def test_content_type(self):
        self.assertEqual(self.formatter.content_type, 'application/json')

    def test_decode(self):
        self.assertEqual(
            self.formatter.decode('value'),
            self.json.loads.return_value)
        # Check json.loads call
        self.json.loads.assert_called_with('value')

    def test_encode(self):
        self.assertEqual(
            self.formatter.encode('value'),
            self.json.dumps.return_value)
        # Check json.dumps call
        self.json.dumps.assert_called_with('value')
