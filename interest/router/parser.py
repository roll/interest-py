from ..helpers import Config


class Parser(Config):
    """Parser representation.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    PATTERN = None
    CONVERT = str
    RESTORE = str

    def __init__(self, service, *,
                 pattern=None, convert=None, restore=None):
        if pattern is None:
            pattern = self.PATTERN
        if convert is None:
            convert = self.CONVERT
        if restore is None:
            restore = self.RESTORE
        assert isinstance(pattern, str)
        assert callable(convert)
        assert callable(restore)
        self.__service = service
        self.__pattern = pattern
        self.__convert = convert
        self.__restore = restore

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

    @property
    def convert(self):
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
        return self.__convert

    @property
    def restore(self):
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
        return self.__restore


class StringParser(Parser):

    # Public

    PATTERN = '[^/]+'


class PathParser(Parser):

    # Public

    PATTERN = r'.*'


class IntegerParser(Parser):

    # Public

    PATTERN = r'[1-9]+'
    CONVERT = int


class FloatParser(Parser):

    # Public

    PATTERN = r'[1-9.]+'
    CONVERT = float
