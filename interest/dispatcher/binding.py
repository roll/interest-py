import asyncio
import inspect
from abc import ABCMeta
from functools import partial
from ..helpers import Function


class Binding(Function, metaclass=ABCMeta):
    """Binding representation (abstract).
    """

    # Public

    MARKER = '_interest.binding'

    def __init__(self, path=''):
        self.__path = path

    def __call__(self, responder):
        if not asyncio.iscoroutinefunction(responder):
            responder = asyncio.coroutine(responder)
        self.__responder = responder
        setattr(responder, self.MARKER, self)
        return responder

    def protocol(self, *args, **kwargs):
        if args and inspect.isfunction(args[0]):
            return Function.FUNCTION
        return Function.DECORATOR

    @property
    def path(self):
        return self.__path

    @property
    def methods(self):
        return [type(self).__name__.upper()]

    @property
    def responder(self):
        return partial(self.__responder, self.resource)


class get(Binding):
    """Binding for the [get] HTTP method.
    """

    # Public

    pass


class post(Binding):
    """Binding for the [post] HTTP method.
    """

    # Public

    pass


class put(Binding):
    """Binding for the [put] HTTP method.
    """

    # Public

    pass


class delete(Binding):
    """Binding for the [delete] HTTP method.
    """

    # Public

    pass


class patch(Binding):
    """Binding for the [patch] HTTP method.
    """

    # Public

    pass


class head(Binding):
    """Binding for the [head] HTTP method.
    """

    # Public

    pass


class options(Binding):
    """Binding for the [options] HTTP method.
    """

    # Public

    pass
