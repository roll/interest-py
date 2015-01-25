import re
from abc import ABCMeta, abstractmethod
from ..helpers import ExistentMatch, NonExistentMatch


class Pattern(metaclass=ABCMeta):

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
            return PlainPattern(pattern, convs)
        else:
            # Regex pattern
            pattern = '/' + '/'.join(parts)
            if path.endswith('/') and pattern != '/':
                pattern += '/'
            return RegexPattern(pattern, convs)

    @abstractmethod
    def match(self, path, prefix=False):
        pass  # pragma: no cover


class PlainPattern(Pattern):

    # Public

    def __init__(self, pattern, convs):
        self.__pattern = pattern
        self.__convs = convs

    def __repr__(self):
        template = '<PlainPattern "{pattern}">'
        compiled = template.format(pattern=self.__pattern)
        return compiled

    def match(self, path, prefix=False):
        match = ExistentMatch()
        if prefix:
            if not path.startswith(self.__pattern):
                return NonExistentMatch()
            return match
        if path != self.__pattern:
            return NonExistentMatch()
        return match


class RegexPattern(Pattern):

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

    def match(self, path, prefix=False):
        match = ExistentMatch()
        pattern = self.__full
        if prefix:
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
