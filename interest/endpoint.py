import asyncio
from .backend import http
from .middleware import Middleware


class Endpoint(Middleware):
    """Endpoint representation.

    .. seealso:: API: :class:`.Middleware`
    """

    # Public

    RESPOND = None

    def __init__(self, service, *,
                 name=None, path=None, methods=None, endpoint=None,
                 respond=None):
        if respond is None:
            respond = self.RESPOND
        super().__init__(service,
            name=name, path=path,
            methods=methods, endpoint=endpoint)
        self.__respond = respond

    @asyncio.coroutine
    def __call__(self, request):
        match = self.service.match(request, path=self.path)
        if match:
            lmatch = self.service.match(request, methods=self.methods)
            if not lmatch:
                raise http.MethodNotAllowed(request.method, self.methods)
            if self.respond is not None:
                return (yield from self.respond(request, **match))
            return (yield from self.process(request))
        return (yield from self.next(request))

    def __repr__(self):
        template = (
            '<Endpoint name="{self.name}" '
            'path="{self.path}" methods="{self.methods}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def respond(self):
        return self.__respond
