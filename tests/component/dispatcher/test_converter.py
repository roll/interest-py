import unittest
from importlib import import_module
component = import_module('interest.dispatcher.converter')


class PatternTest(unittest.TestCase):

    # Tests

    def test_string(self):
        converter = component.StringConverter()
        pattern = '^' + converter.pattern + '$'
        self.assertRegex('string', pattern)
        self.assertNotRegex('string/', pattern)
        self.assertEqual(converter.convert('string'), 'string')

    def test_integer(self):
        converter = component.IntegerConverter()
        pattern = '^' + converter.pattern + '$'
        self.assertRegex('1', pattern)
        self.assertNotRegex('1/', pattern)
        self.assertEqual(converter.convert('1'), 1)

    def test_float(self):
        converter = component.FloatConverter()
        pattern = '^' + converter.pattern + '$'
        self.assertRegex('1.1', pattern)
        self.assertNotRegex('1.1/', pattern)
        self.assertEqual(converter.convert('1.1'), 1.1)

    def test_path(self):
        converter = component.PathConverter()
        pattern = '^' + converter.pattern + '$'
        self.assertRegex('my/path', pattern)
        self.assertNotRegex('my/path>', pattern)
        self.assertEqual(converter.convert('my/path'), 'my/path')
