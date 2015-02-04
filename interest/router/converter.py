from ..helpers import Configurable


class Converter(Configurable):
    """Converter representation.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    PATTERN = None
    CONVERT = None

    def __init__(self, router, *, pattern=None, convert=None):
        if pattern is None:
            pattern = self.PATTERN
        if convert is None:
            convert = self.CONVERT
        assert pattern is not None
        assert convert is not None
        self.__service = router.service
        self.__router = router
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
    def router(self):
        """:class:`.Router` instance (read-only).
        """
        return self.__router

    @property
    def pattern(self):
        """Converter's pattern (read-only).
        """
        return self.__pattern

    def convert(self, string):
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
        return self.__convert(string)
