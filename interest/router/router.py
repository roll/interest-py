from abc import ABCMeta, abstractmethod
from ..helpers import Configurable


class Router(Configurable, metaclass=ABCMeta):
    """Router representation.
    """

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @abstractmethod
    def build(self, *args, **kwargs):
        pass  # pragma: no cover

    @abstractmethod
    def match(self, request, *, root=None, path=None, methods=None):
        """Check if request matchs the given parameters.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        root: str
            HTTP path root.
        path: str
            HTTP path.
        methods: list
            HTTP methods.

        Returns
        -------
        :class:`.Match`
            Match instance.
        """
        pass  # pragma: no cover
