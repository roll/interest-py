from ..helpers import Config


class Parser(Config):
    """Parser is a component responsible for the parsing.

    Router uses a parsers dictionary to handle user placeholders in paths.
    Placeholder is a path insertion in following form "<name:parser>".

    .. seealso:: Implements:
        :class:`.Config`

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    pattern: str
        Regex pattern to match.
    convert: callable
        Callable to convert a string to a value.
    restore: callable
        Callable to restore a string from a value.

    Examples
    --------
    Let's create a binary parser::

        class BinaryParser(Parser):

            # Public

            PATTERN = r'[01]+'
            CONVERT = int

        router = Router(parsers={'bin': BinaryParser})
        router.match('<request>', '/some/path/<name:bin>')
    """

    # Public

    PATTERN = None
    """Default pattern parameter.
    """
    CONVERT = str
    """Default convert parameter.
    """
    RESTORE = str
    """Default restore parameter.
    """

    def __init__(self, service, *,
                 pattern=None, convert=None, restore=None):
        if pattern is None:
            pattern = self.PATTERN
        if convert is None:
            convert = self.CONVERT
        if restore is None:
            restore = self.RESTORE
        self.__service = service
        self.__pattern = pattern
        assert isinstance(self.pattern, str)
        # Override attributes
        if convert is not None:
            self.convert = convert
        if restore is not None:
            self.restore = restore

    def __repr__(self):
        template = (
            '<Parser pattern="{self.pattern}" '
            'convert="{self.convert}" '
            'restore="{self.restore}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def pattern(self):
        """Parser's pattern (read-only).
        """
        return self.__pattern

    def convert(self, string):
        """Convert a given string to a value.

        Parameters
        ----------
        string: str
            String to convert.

        Returns
        -------
        object
            Converted string.
        """
        raise NotImplementedError()

    def restore(self, value):
        """Restore a given value to a string.

        Parameters
        ----------
        value: object
            Value to restore.

        Returns
        -------
        str
            Restored string.
        """
        raise NotImplementedError()


class StringParser(Parser):

    # Public

    PATTERN = '[^/]+'


class PathParser(Parser):

    # Public

    PATTERN = r'.*'


class IntegerParser(Parser):

    # Public

    PATTERN = r'[0-9]+'
    CONVERT = int


class FloatParser(Parser):

    # Public

    PATTERN = r'[0-9.]+'
    CONVERT = float
