import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.router.converter')


class ConverterTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.router = Mock()
        self.convert = Mock()
        self.converter = component.Converter(
            self.router, pattern='pattern', convert=self.convert)

    # Tests

    def test_service(self):
        self.assertEqual(self.converter.service, self.router.service)

    def test_router(self):
        self.assertEqual(self.converter.router, self.router)

    def test_pattern(self):
        self.assertEqual(self.converter.pattern, 'pattern')

    def test_convert(self):
        self.assertEqual(
            self.converter.convert('string'),
            self.convert.return_value)
        # Check convert call
        self.convert.assert_called_with('string')
