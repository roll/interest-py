import asyncio
import inspect
from .endpoint import Endpoint
from .helpers import Chain, OrderedMetaclass
from .middleware import Middleware
from .protocol import http


class Resource(Chain, Middleware, metaclass=OrderedMetaclass):
    """Resource representation (abstract).
    """

    # Public

    def __init__(self, service, *, name=None, path=None, methods=None):
        super().__init__(service, name=name, path=path, methods=methods)
        self.__add_endpoints()

    def __repr__(self):
        template = (
            '<Resource path="{self.path}" '
            'methods="{self.methods}" '
            'endpoints={endpoints}>')
        compiled = template.format(
            self=self, endpoints=list(self))
        return compiled

    @asyncio.coroutine
    def process(self, request):
        for endpoint in self:
            path = self.path + endpoint.path
            match = self.service.match(request, path=path)
            if not match:
                continue
            check = self.service.match(request, methods=endpoint.methods)
            if not check:
                raise http.MethodNotAllowed(request.method, endpoint.methods)
            return (yield from endpoint(request, **match))
        raise http.NotFound()

    # Private

    def __add_endpoints(self):
        for name in self.__order__:
            if name.startswith('_'):
                continue
            func = getattr(type(self), name)
            if inspect.isdatadescriptor(func):
                continue
            constraints = getattr(func, http.MARKER, None)
            if constraints is not None:
                endpoint = Endpoint(self, name=name, **constraints)
                self._append(endpoint, name=endpoint.name)
