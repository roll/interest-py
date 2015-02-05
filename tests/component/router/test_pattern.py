import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.router.pattern')


class PatternTest(unittest.TestCase):

    # Helpers

    S = component.StringPattern
    R = component.RegexPattern
    E = Exception
    N = None

    parsers = {
        # Meta, instance
        'str': Mock(pattern=r'[^<>/]+', convert=str),
        'int': Mock(pattern=r'[1-9/]+', convert=int),
        'float': Mock(pattern=r'[1-9./]+', convert=float),
        'path': Mock(pattern=r'[^<>]+', convert=str),
    }

    fixtures = [
        # Pattern, string, left, match, type/exception
        ['/test', '/test2', False, N, S],
        ['/test', '/test', False, {}, S],
        ['/<key>', '/value', False, {'key': 'value'}, R],
        ['/<key:str>', '/5', False, {'key': '5'}, R],
        ['/<key:int>', '/5', False, {'key': 5}, R],
        ['/<key:float>', '/5.5', False, {'key': 5.5}, R],
        ['/<key:path>', '/my/path', False, {'key': 'my/path'}, R],
    ]

    # Tests

    def test(self):
        for fixture in self.fixtures:
            (pattern, string, left, match, tex) = fixture
            if issubclass(tex, Exception):
                self.assertRaises(tex,
                    component.Pattern.create, pattern, self.parsers)
                continue
            pattern = component.Pattern.create(pattern, self.parsers)
            self.assertIsInstance(pattern, tex, (pattern, fixture))
            self.assertEqual(
                pattern.match(string, left),
                match, (pattern, fixture))
