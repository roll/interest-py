import asyncio
import inspect
from abc import ABCMeta
from functools import partial
from sugarbowl import Function


class Binding(Function, metaclass=ABCMeta):
    """Binding representation.
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

    def register(self, *, service, resource, dispatcher):
        method = type(self).__name__.lower()
        fullpath = service.path + resource.path + self.__path
        bresponder = partial(self.__responder, resource)
        dispatcher.add_route(method, fullpath, bresponder)


class get(Binding):
    """HTTP method get representation.
    """

    # Public

    pass


class post(Binding):
    """HTTP method post representation.
    """

    # Public

    pass


class put(Binding):
    """HTTP method put representation.
    """

    # Public

    pass


class delete(Binding):
    """HTTP method delete representation.
    """

    # Public

    pass


class patch(Binding):
    """HTTP method patch representation.
    """

    # Public

    pass


class head(Binding):
    """HTTP method head representation.
    """

    # Public

    pass


class options(Binding):
    """HTTP method options representation.
    """

    # Public

    pass
