import asyncio
from abc import ABCMeta, abstractmethod


class Route(dict, metaclass=ABCMeta):
    """Route representation.
    """

    # Public

    @abstractmethod
    def __bool__(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def responder(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def match(self):
        pass  # pragma: no cover


class ExistentRoute(Route):
    """ExistentRoute representation.
    """

    # Public

    def __init__(self, responder, match):
        self.__responder = responder
        self.__match = match

    def __bool__(self):
        return True

    @property
    def responder(self):
        return self.__responder

    @property
    def match(self):
        return self.__match


class NonExistentRoute(Route):
    """NonExistentRoute representation.
    """

    # Public

    def __init__(self, exception):
        self.__exception = exception

    def __bool__(self):
        return False

    @asyncio.coroutine
    def responder(self, *args, **kwargs):
        raise self.__exception

    @property
    def match(self):
        return {}
