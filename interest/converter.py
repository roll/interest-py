from .helpers import Configurable


class Converter(Configurable):
    """Converter representation.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    PATTERN = r'[1-9]+'
    CONVERT = str

    def __init__(self, service, *, pattern=None, convert=None):
        if pattern is None:
            pattern = self.PATTERN
        if convert is None:
            convert = self.CONVERT
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
        """Converter's pattern.
        """
        return self.__pattern

    def convert(self, string):
        """Convert the given string.

        Parameters
        ----------
        string: str
            String to convert.

        Returns
        -------
        object
            Converted string.
        """
        return self.__convert(string)
