import asyncio
from abc import ABCMeta
from ..helpers import Configurable


class Handler(Configurable, asyncio.Protocol, metaclass=ABCMeta):

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def fork(self):
        """Handler factory for asyncio's loop.create_server.
        """
        return type(self)(self.service)
