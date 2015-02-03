import asyncio
from abc import ABCMeta, abstractmethod
from .helpers import Configurable


class Provider(Configurable, metaclass=ABCMeta):

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @abstractmethod
    @asyncio.coroutine
    def provide(self):
        pass  # pragma: no cover
