import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.router.parser')


class ParserTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.convert = Mock()
        self.parser = component.Parser(
            'service', pattern='pattern', convert=self.convert)

    # Tests

    def test_service(self):
        self.assertEqual(self.parser.service, 'service')

    def test_pattern(self):
        self.assertEqual(self.parser.pattern, 'pattern')

    def test_convert(self):
        self.assertEqual(
            self.parser.convert('string'),
            self.convert.return_value)
        # Check convert call
        self.convert.assert_called_with('string')
