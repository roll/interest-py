import asyncio
from .backend import http
from .middleware import Middleware


class Endpoint(Middleware):
    """Endpoint is a middleware capable to respont to a request.

    Enpoint is used by :meth:`.http.bind` methods family to convert
    middleware's methods to the middleware's endpoints.
    Usually user application never creates enpoints by itself.

    .. seealso:: Implements:
        :class:`.Middleware`,
        :class:`.Chain`,
        :class:`.Config`

    Parameters
    ----------
    respond: coroutine
        Coroutine to respond to a request.
    extra: dict
        Extra arguments.

    Examples
    --------
    Let see how to get access to an endpoint::

        class Middleware(Middleware):

            # Public

            @http.get('/<text:path>')
            def echo(self, request, text):
                return http.Response(text=text)

        endpoint = Middleware('<service>')['echo']
        response = yield from endpoint('<request>')
    """

    # Public

    RESPOND = None
    """Default respond parameter.
    """

    def __init__(self, service, *,
                 name=None, prefix=None, methods=None, endpoint=None,
                 respond=None, **extra):
        if respond is None:
            respond = self.RESPOND
        super().__init__(service,
            name=name, prefix=prefix,
            methods=methods, endpoint=endpoint)
        # Override attributes
        if respond is not None:
            self.respond = respond
        self.__extra = extra

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
    def extra(self):
        """Dict if extra arguments passed to the endpoint.
        """
        return self.__extra

    @asyncio.coroutine
    def respond(self, request, **kwargs):
        """Respond to a request (coroutine).

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        kwargs: dict
            Keyword arguments.

        Returns
        -------
        object
            Reply value.
        """
        raise http.NotFound()
