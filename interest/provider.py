import asyncio
from functools import partial
from abc import ABCMeta, abstractmethod


class Provider(metaclass=ABCMeta):

    # Public

    def __init__(self, service):
        self.__service = service

    @classmethod
    def config(cls, **kwargs):
        return partial(cls, **kwargs)

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @abstractmethod
    @asyncio.coroutine
    def provide(self):
        pass  # pragma: no cover
