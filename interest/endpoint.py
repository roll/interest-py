import asyncio
from .helpers import Configurable, name


class Endpoint(Configurable):

    # Public

    NAME = name
    PATH = ''
    METHODS = None

    def __init__(self, resource, *, name=None, path=None, methods=None):
        if name is None:
            name = self.NAME
        if path is None:
            path = self.PATH
        if methods is None:
            methods = self.METHODS
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
    def resource(self):
        return self.__resource

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def methods(self):
        return self.__methods
