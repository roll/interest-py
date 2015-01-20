from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    """Formatter base class (abstract).

    Formatter is NOT used by :class:`.Service`. But it presents as
    service's attribute for user needs. Formatter is responsible for
    data converting from data to string and vice versa. Also formatter
    provides corresponding content type.
    For example see :class:`.JSONFormatter`.

    Example
    -------
    Let's say we want a toy python formatter::

        class PythonFormatter(Formatter):

            # Public

            content_type = 'application/python' # Don't try this at home!

            def encode(self, data):
                return str(data)

            def decode(self, text):
                return text

        service = Service(path='/api/v1', formatter=PythonFormatter)

    Probably in some middleware we will use it::

        >>> service.formatter.encode({'hello': 'world'})
        "{'hello': 'world'}"
        >>> service.formatter.decode('noop')
        'noop'
        >>> service.formatter.content_type
        'application/python'

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    @abstractmethod
    def content_type(self):
        """Content-type for encoded data (read-only) (abstract).
        """
        pass  # pragma: no cover

    @abstractmethod
    def decode(self, text):
        """Decode text (abstract).

        Parameters
        ----------
        text: str
            Text to decode.

        Returns
        -------
        dict:
            Data decoded from the string.
        """
        pass  # pragma: no cover

    @abstractmethod
    def encode(self, data):
        """Encode data (abstract).

        Parameters
        ----------
        data: dict
            Data to encode.

        Returns
        -------
        str:
            Data encoded to the string.
        """
        pass  # pragma: no cover
