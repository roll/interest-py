import asyncio
from .backend import http
from .helpers import Configurable, NonExistentMatch, name


class Endpoint(Configurable):
    """Endpoint representation.
    """

    # Public

    NAME = name
    PATH = ''
    METHODS = []

    def __init__(self, resource, *, name=None, path=None, methods=None):
        if name is None:
            name = self.NAME
        if path is None:
            path = self.PATH
        if methods is None:
            methods = self.METHODS
        path = resource.path + path
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
            '<Endpoint path="{self.path}" '
            'methods="{self.methods}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        return self.__resource.service

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

    def match(self, request):
        match = self.service.router.match(request, path=self.path)
        if not match:
            return NonExistentMatch()
        lmatch = self.service.router.match(request, methods=self.methods)
        if not lmatch:
            raise http.MethodNotAllowed(request.method, self.methods)
        return match
