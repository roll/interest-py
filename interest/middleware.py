import asyncio
import inspect
from .backend import http
from .helpers import Chain, Config, OrderedMetaclass, STICKER, name


class Middleware(Chain, Config, metaclass=OrderedMetaclass):
    """Middleware is a extended coroutine to process requests.

    Middleware is a key concept of the interest. For example
    :class:`.Service` and :class:`.Endpoint` are the Middlewares.
    The interest framework uses middlewares only as coroutines
    calling :meth:`.Middleware.__call__` method.
    But user application may use all provided API because of
    knowledge of the application topology.

    .. seealso:: Implements:
        :class:`.Chain`,
        :class:`.Config`

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    name: str
        Middleware's name.
    prefix: str
        HTTP path prefix constraint.
    methods: list
        HTTP methods allowed constraint.
    middlewares: list
        List of submiddlewares.
    endpoint: :class:`.Endpoint` subclass.
        Default endpoint class for bindings.

    Examples
    --------
    Processing middleware::

        class Middleware(Middleware):

            # Public

            @asyncio.coroutine
            def process(self, request):
                try:
                    # Process request here
                    response = yield from self.next(request)
                    # Process response here
                except http.Exception as exception:
                    # Process exception here
                    response = exception
                return response

        middleware = Middleware('<service>')
        response = yield from middleware('<request>')
    """

    # Public

    NAME = name
    """Default name parameter.
    """
    PREFIX = ''
    """Default prefix parameter.
    """
    METHODS = []
    """Default methods parameter.
    """
    MIDDLEWARES = []
    """Default middlewares parameter.
    """
    ENDPOINT = None
    """Default endpoint parameter.
    """

    def __init__(self, service, *,
                 name=None, prefix=None, methods=None,
                 middlewares=None, endpoint=None):
        if name is None:
            name = self.NAME
        if prefix is None:
            prefix = self.PREFIX
        if methods is None:
            methods = self.METHODS.copy()
        if middlewares is None:
            middlewares = self.MIDDLEWARES.copy()
        if endpoint is None:
            endpoint = self.ENDPOINT
        if endpoint is None:
            from .endpoint import Endpoint
            endpoint = Endpoint
        self.main = self
        self.over = self
        super().__init__()
        self.__service = service
        self.__name = name
        self.__prefix = prefix
        self.__methods = methods
        self.__endpoint = endpoint
        self.__add_middlewares(middlewares)
        self.__add_endpoints()

    @asyncio.coroutine
    def __call__(self, request):
        """Process a request (coroutine).

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.

        Returns
        -------
        object
            Reply value.
        """
        match = self.service.match(
            request, root=self.path, methods=self.methods)
        if match:
            return (yield from self.process(request))
        return (yield from self.next(request))

    def __repr__(self):
        template = (
            '<Middleware name="{self.name}" '
            'path="{self.path}" methods="{self.methods}" '
            'middlewares={middlewares}>')
        compiled = template.format(
            self=self, middlewares=list(self))
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def name(self):
        """Middleware's name (read-only).
        """
        return self.__name

    @property
    def path(self):
        """HTTP full path constraint. (read-only).
        """
        path = self.__prefix
        if self is not self.over:
            path = self.over.path + path
        return path

    @property
    def methods(self):
        """HTTP methods allowed constraint (read-only).
        """
        return self.__methods

    @asyncio.coroutine
    def process(self, request):
        """Process a request (coroutine).

        .. note:: This coroutine will be reached only if request
            matches :attr:`.path` and :attr:`.methods` constraints.

        By default this method sends request to submiddleware chain and
        returns reply. It's standard point to override Middleware behavior
        by user application.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.

        Returns
        -------
        object
            Reply value.
        """
        if self:
            return (yield from self[0](request))
        raise http.NotFound()

    @asyncio.coroutine
    def main(self, request):
        """Link to the main middleware (coroutine).
        """
        raise http.NotFound()

    @asyncio.coroutine
    def over(self, request):
        """Link to the over middleware (coroutine).
        """
        raise http.NotFound()

    @asyncio.coroutine
    def prev(self, request):
        """Link to the previous middleware (coroutine).
        """
        raise http.NotFound()

    @asyncio.coroutine
    def next(self, request):
        """Link to the next middleware (coroutine).
        """
        raise http.NotFound()

    # Internal (Chain's hooks)

    def push(self, item, *, index=None):
        super().push(item, index=index)
        self.__update_topology()

    def pull(self, *, index=None):
        super().pull(index=index)
        self.__update_topology()

    # Private

    def __add_middlewares(self, middlewares):
        for middleware in middlewares:
            if not asyncio.iscoroutine(middleware):
                middleware = middleware(self.service)
            self.push(middleware)

    def __add_endpoints(self):
        for name in self.__order__:
            if name.startswith('_'):
                continue
            func = getattr(type(self), name)
            if inspect.isdatadescriptor(func):
                continue
            bindings = getattr(func, STICKER, [])
            for binding in reversed(bindings):
                factory = binding.pop(
                    'endpoint', self.__endpoint)
                respond = getattr(self, name)
                endpoint = factory(self.service,
                    name=name, respond=respond, **binding)
                self.push(endpoint)

    def __update_topology(self):
        for index, middleware in enumerate(self):
            if isinstance(middleware, Middleware):
                # Override attributes
                middleware.main = self.main
                middleware.over = self
                if index - 1 > -1:
                    middleware.prev = self[index - 1]
                if index + 1 < len(self):
                    middleware.next = self[index + 1]
                middleware.__update_topology()
