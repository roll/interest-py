import asyncio
from .helpers import Configurable


class Endpoint(Configurable):

    # Public

    # TODO: decide about None defaults
    def __init__(self, resource, *, name, path=None, methods=None):
        self.__resource = resource
        self.__name = name
        self.__path = path
        self.__methods = methods
        self.__coroutine = getattr(resource, name)

    @asyncio.coroutine
    def __call__(self, request, **kwargs):
        return (yield from self.__coroutine(request, **kwargs))

    def __repr__(self):
        template = (
            '<Endpoint path="{self.path}" methods="{self.methods}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def methods(self):
        return self.__methods
