import asyncio
from abc import ABCMeta
from ..helpers import Configurable


class Handler(Configurable, asyncio.Protocol, metaclass=ABCMeta):
    """Handler representation (abstract).
    """

    # Public

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self.__args = args
        self.__kwargs = kwargs
        return self

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
        return type(self)(*self.__args, **self.__kwargs)
