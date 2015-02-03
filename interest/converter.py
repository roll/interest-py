from abc import ABCMeta, abstractmethod
from .helpers import Configurable


class Converter(Configurable, metaclass=ABCMeta):
    """Converter representation (abstract).

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        self.__service = service

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
    @abstractmethod
    def pattern(self):
        """Converter's pattern.
        """
        pass  # pragma: no cover

    @abstractmethod
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
        pass  # pragma: no cover


class StringConverter(Converter):

    # Public

    pattern = r'[^<>/]+'
    convert = str


class IntegerConverter(Converter):

    # Public

    pattern = r'[1-9]+'
    convert = int


class FloatConverter(Converter):

    # Public

    pattern = r'[1-9.]+'
    convert = float


class PathConverter(Converter):

    # Public

    pattern = r'[^<>]+'
    convert = str
