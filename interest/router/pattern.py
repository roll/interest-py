import re
from abc import ABCMeta, abstractmethod
from ..helpers import Match


class Pattern(metaclass=ABCMeta):
    """Pattern representation (abstract).
    """

    # Public

    @abstractmethod
    def match(self, string, left=False):
        pass  # pragma: no cover

    @abstractmethod
    def format(self, **match):
        pass  # pragma: no cover

    @classmethod
    def create(cls, pattern, parsers):
        matches = list(cls.__PARSER_PATTERN.finditer(pattern))
        if not matches:
            return StringPattern(pattern)
        lastend = 0
        cpattern = ''
        cparsers = {}
        template = ''
        for match in matches:
            name = match.group('name')
            meta = match.group('meta')
            if meta is None:
                meta = 'str'
            if meta not in parsers:
                raise ValueError(
                    'Unsupported parser {meta}'.format(meta=meta))
            parser = parsers[meta]
            before = pattern[lastend:match.start()]
            cpattern += cls.__pattern_escape(before)
            cpattern += cls.__PARSER_TEMPLATE.format(
                name=name, parser=parser)
            cparsers[name] = parser
            template += cls.__template_escape(before)
            template += '{' + name + '}'
            lastend = match.end()
        after = pattern[lastend:]
        cpattern += re.escape(after)
        template += after
        return RegexPattern(cpattern, cparsers, template)

    # Private

    __PARSER_PATTERN = re.compile(r'\<(?P<name>\w+)(?::(?P<meta>\w+))?\>')
    __PARSER_TEMPLATE = '(?P<{name}>{parser.pattern})'

    @classmethod
    def __pattern_escape(cls, pattern):
        pattern = re.escape(pattern)
        return pattern

    @classmethod
    def __template_escape(cls, template):
        template = template.replace('{', '{{')
        template = template.replace('}', '}}')
        return template


class StringPattern(Pattern):

    # Public

    def __init__(self, pattern):
        self.__pattern = pattern

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

    def __init__(self, pattern, parsers, template):
        self.__pattern = pattern
        self.__parsers = parsers
        self.__template = template
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
            try:
                value = self.__parsers[name].convert(string)
            except Exception:
                return None
            match[name] = value
        return match

    def format(self, **match):
        for name, value in match.items():
            match[name] = self.__parsers[name].restore(value)
        return self.__template.format_map(match)
