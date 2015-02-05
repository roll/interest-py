import re
from abc import ABCMeta, abstractmethod
from ..helpers import ExistentMatch, NonExistentMatch


class Matcher(metaclass=ABCMeta):
    """Matcher representation (abstract).
    """

    # Public

    PLAIN_PATTERN = re.compile('^[^<>/]+$')
    REGEX_PATTERN = re.compile(r'^\<(?P<name>\w+)(?::(?P<meta>\w+))?\>$')
    REGEX_TEMPLATE = '(?P<{name}_{meta}>{conv.pattern})'

    @classmethod
    def create(cls, path, convs):
        parts = []
        plain = True
        for part in path.split('/'):
            if not part:
                continue
            # Check regex pattern
            match = cls.REGEX_PATTERN.match(part)
            if match:
                name = match.group('name')
                meta = match.group('meta')
                if meta is None:
                    meta = 'str'
                try:
                    conv = convs[meta]
                except KeyError:
                    raise ValueError(
                        'Unsupported converter {meta}'.format(meta=meta))
                part = cls.REGEX_TEMPLATE.format(
                    name=name, meta=meta, conv=conv)
                parts.append(part)
                plain = False
                continue
            # Check plain pattern
            match = cls.PLAIN_PATTERN.match(part)
            if match:
                parts.append(re.escape(part))
                continue
            raise ValueError('Invalid path "{path}"'.format(path=path))
        if plain:
            # Plain pattern
            pattern = path
            return PlainMatcher(pattern, convs)
        else:
            # Regex pattern
            pattern = '/' + '/'.join(parts)
            if path.endswith('/') and pattern != '/':
                pattern += '/'
            return RegexMatcher(pattern, convs)

    @abstractmethod
    def match(self, path, left=False):
        pass  # pragma: no cover


class PlainMatcher(Matcher):

    # Public

    def __init__(self, pattern, convs):
        self.__pattern = pattern
        self.__convs = convs

    def __repr__(self):
        template = '<PlainMatcher "{pattern}">'
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


class RegexMatcher(Matcher):

    # Public

    def __init__(self, pattern, convs):
        self.__pattern = pattern
        self.__convs = convs
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
                value = self.__convs[meta].convert(value)
            except Exception:
                return NonExistentMatch()
            match[name] = value
        return match
