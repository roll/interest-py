import re
from abc import ABCMeta, abstractmethod
from ..helpers import Match


class Pattern(metaclass=ABCMeta):
    """Pattern representation (abstract).
    """

    # Public

    PARSER_PATTERN = re.compile(r'\<(?P<name>\w+)(?::(?P<meta>\w+))?\>')
    PARSER_TEMPLATE = '(?P<{name}_{meta}>{parser.pattern})'

    @classmethod
    def create(cls, pattern, parsers):
        matches = list(cls.PARSER_PATTERN.finditer(pattern))
        if not matches:
            return StringPattern(pattern, parsers)
        lastend = 0
        storage = ''
        for match in matches:
            name = match.group('name')
            meta = match.group('meta')
            if meta is None:
                meta = 'str'
            if meta not in parsers:
                raise ValueError(
                    'Unsupported parser {meta}'.format(meta=meta))
            parser = parsers[meta]
            storage += re.escape(pattern[lastend:match.start()])
            storage += cls.PARSER_TEMPLATE.format(
                name=name, meta=meta, parser=parser)
            lastend = match.end()
        storage += re.escape(pattern[lastend:])
        return RegexPattern(storage, parsers)

    @abstractmethod
    def match(self, string, left=False):
        pass  # pragma: no cover

    @abstractmethod
    def format(self, **match):
        pass  # pragma: no cover


class StringPattern(Pattern):

    # Public

    def __init__(self, pattern, parsers):
        self.__pattern = pattern
        self.__parsers = parsers

    def __repr__(self):
        template = '<StringPattern "{pattern}">'
        compiled = template.format(pattern=self.__pattern)
        return compiled

    def match(self, string, left=False):
        match = Match()
        if left:
            if not string.startswith(self.__pattern):
                return None
            return match
        if string != self.__pattern:
            return None
        return match

    def format(self, **match):
        return self.__pattern


class RegexPattern(Pattern):

    # Public

    def __init__(self, pattern, parsers):
        self.__pattern = pattern
        self.__parsers = parsers
        try:
            self.__left = re.compile('^' + pattern)
            self.__full = re.compile('^' + pattern + '$')
        except re.error:
            raise ValueError(
                'Invalid pattern "{pattern}"'.
                format(pattern=pattern))

    def __repr__(self):
        template = '<RegexPattern "{pattern}">'
        compiled = template.format(pattern=self.__pattern)
        return compiled

    def match(self, string, left=False):
        match = Match()
        pattern = self.__full
        if left:
            pattern = self.__left
        result = pattern.match(string)
        if not result:
            return None
        for name, string in result.groupdict().items():
            name, meta = name.rsplit('_', 1)
            try:
                value = self.__parsers[meta].convert(string)
            except Exception:
                return None
            match[name] = value
        return match

    def format(self, **match):
        raise NotImplementedError()
