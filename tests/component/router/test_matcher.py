import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.router.matcher')


class MatcherTest(unittest.TestCase):

    # Helpers

    P = component.PlainMatcher
    R = component.RegexMatcher
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
        # Matcher, path, left, match, type/exception
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
            (matcher, path, left, match, tex) = fixture
            if issubclass(tex, Exception):
                self.assertRaises(tex,
                    component.Matcher.create, matcher, self.converters)
                continue
            matcher = component.Matcher.create(matcher, self.converters)
            self.assertIsInstance(matcher, tex, (matcher, fixture))
            self.assertEqual(
                matcher.match(path, left),
                match, (matcher, fixture))
