from ..helpers import Config


class Converter(Config):
    """Converter representation.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    PATTERN = None
    CONVERT = None

    def __init__(self, service, *, pattern=None, convert=None):
        if pattern is None:
            pattern = self.PATTERN
        if convert is None:
            convert = self.CONVERT
        assert pattern is not None
        assert convert is not None
        self.__service = service
        self.__pattern = pattern
        self.__convert = convert

    def __repr__(self):
        template = (
            '<Converter pattern="{self.pattern}" '
            'convert="{self.convert}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def pattern(self):
        """Converter's pattern (read-only).
        """
        return self.__pattern

    @property
    def convert(self):
        """Convert the given string (read-only).

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
