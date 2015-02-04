import asyncio
from abc import ABCMeta, abstractmethod
from .helpers import Configurable


class Provider(Configurable, metaclass=ABCMeta):
    """Provider representation (abstract).
    """

    # Public

    def __init__(self, service):
        self.__service = service

    def __repr__(self):
        template = '<Provider provide="{self.provide}">'
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @abstractmethod
    @asyncio.coroutine
    def provide(self):
        pass  # pragma: no cover
