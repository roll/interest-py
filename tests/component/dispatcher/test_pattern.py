import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.dispatcher.pattern')


class PatternTest(unittest.TestCase):

    # Helpers

    P = component.PlainPattern
    R = component.RegexPattern
    N = component.NonExistentMatch()
    E = Exception

    converters = {
        # Meta, instance
        'str': Mock(pattern=r'[^<>/]+', convert=str),
        'int': Mock(pattern=r'[1-9/]+', convert=int),
        'float': Mock(pattern=r'[1-9./]+', convert=float),
        'path': Mock(pattern=r'[^<>]+', convert=str),
    }

    fixtures = [
        # Pattern, path, left, match, type/exception
        ['/<>', None, None, None, E],
        ['/test', '/test2', False, N, P],
        ['/test', '/test', False, {}, P],
        ['/<key>', '/value', False, {'key': 'value'}, R],
        ['/<key:str>', '/5', False, {'key': '5'}, R],
        ['/<key:int>', '/5', False, {'key': 5}, R],
        ['/<key:float>', '/5.5', False, {'key': 5.5}, R],
        ['/<key:path>', '/my/path', False, {'key': 'my/path'}, R],
    ]

    # Tests

    def test(self):
        for fixture in self.fixtures:
            (pattern, path, left, match, tex) = fixture
            if issubclass(tex, Exception):
                self.assertRaises(tex,
                    component.Pattern.create, pattern, self.converters)
                continue
            pattern = component.Pattern.create(pattern, self.converters)
            self.assertIsInstance(pattern, tex, (pattern, fixture))
            self.assertEqual(
                pattern.match(path, left),
                match, (pattern, fixture))
