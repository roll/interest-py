import re
from abc import ABCMeta, abstractmethod
from ..helpers import ExistentMatch, NonExistentMatch


class Pattern(metaclass=ABCMeta):
    """Pattern representation (abstract).
    """

    # Public

    PARSER_PATTERN = re.compile(r'\<(?P<name>\w+)(?::(?P<meta>\w+))?\>')
    PARSER_TEMPLATE = '(?P<{name}_{meta}>{parser.pattern})'

    @classmethod
    def create(cls, path, parsers):
        matches = list(cls.PARSER_PATTERN.finditer(path))
        if not matches:
            return PlainPattern(path, parsers)
        lastend = 0
        pattern = ''
        for match in matches:
            name = match.group('name')
            meta = match.group('meta')
            if meta is None:
                meta = 'str'
            if meta not in parsers:
                raise ValueError(
                    'Unsupported parser {meta}'.format(meta=meta))
            parser = parsers[meta]
            pattern += re.escape(path[lastend:match.start()])
            pattern += cls.PARSER_TEMPLATE.format(
                name=name, meta=meta, parser=parser)
            lastend = match.end()
        pattern += re.escape(path[lastend:])
        return RegexPattern(pattern, parsers)

    @abstractmethod
    def build(self, *args, **kwargs):
        pass  # pragma: no cover

    @abstractmethod
    def match(self, path, left=False):
        pass  # pragma: no cover


class PlainPattern(Pattern):

    # Public

    def __init__(self, pattern, parsers):
        self.__pattern = pattern
        self.__parsers = parsers

    def __repr__(self):
        template = '<PlainPattern "{pattern}">'
        compiled = template.format(pattern=self.__pattern)
        return compiled

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    def match(self, path, left=False):
        match = ExistentMatch()
        if left:
            if not path.startswith(self.__pattern):
                return NonExistentMatch()
            return match
        if path != self.__pattern:
            return NonExistentMatch()
        return match


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

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    def match(self, path, left=False):
        match = ExistentMatch()
        pattern = self.__full
        if left:
            pattern = self.__left
        result = pattern.match(path)
        if not result:
            return NonExistentMatch()
        for name, value in result.groupdict().items():
            name, meta = name.rsplit('_', 1)
            try:
                value = self.__parsers[meta].convert(value)
            except Exception:
                return NonExistentMatch()
            match[name] = value
        return match
