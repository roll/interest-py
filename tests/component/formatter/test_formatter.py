import unittest
from importlib import import_module
component = import_module('interest.formatter.formatter')


class FormatterTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.Formatter = self.make_mock_formatter_class()
        self.formatter = self.Formatter('service')

    # Helpers

    def make_mock_formatter_class(self):
        class MockFormatter(component.Formatter):
            # Public
            content_type = 'content_type'
            decode = 'decode'
            encode = 'encode'
        return MockFormatter

    # Tests

    def test_service(self):
        self.assertEqual(self.formatter.service, 'service')

    def test_abstract(self):
        self.assertRaises(TypeError, component.Formatter, 'service')
