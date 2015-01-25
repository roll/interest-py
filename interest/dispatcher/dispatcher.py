import asyncio
from ..helpers import Chain, ExistentMatch, NonExistentMatch, http
from .pattern import Pattern
from .route import ExistentRoute, NonExistentRoute
from .converter import (FloatConverter, IntegerConverter,
                        PathConverter, StringConverter)

class Dispatcher:
    """Dispatcher representation.

    Dispatcher is used by :class:`.Service` to dispatch requests.
    Dispatcher presents as service's attribute for the user routing needs.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__resources = Chain()
        self.__converters = Chain()
        self.__patterns = {}
        # Add default converters
        self.__add_converters()

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def resources(self):
        """:class:`.Chain` of resources.
        """
        return self.__resources

    @property
    def converters(self):
        """:class:`.Chain` of converters.
        """
        return self.__converters

    @asyncio.coroutine
    def dispatch(self, request):
        """Dispatch a request.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.

        Returns
        -------
        :class:`.Route`
            Route instance.
        """
        route = NonExistentRoute(http.NotFound())
        # Check the service
        path = self.service.path
        match = self.__match_path(request, path, prefix=True)
        if not match:
            return route
        # Check the resources
        match = False
        for resource in self.resources:
            path = self.service.path + resource.path
            match = self.__match_path(request, path, prefix=True)
            if match:
                break
        if not match:
            return route
        # Check the bingings
        for binding in resource.bindings:
            path = self.service.path + resource.path + binding.path
            match1 = self.__match_path(request, path)
            if not match1:
                continue
            match2 = self.__match_methods(request, binding.methods)
            if not match2:
                return NonExistentRoute(
                    http.MethodNotAllowed(request.method, binding.methods))
            return ExistentRoute(binding.responder, match1)
        return route

    def match(self, request, *, path=None, methods=None, prefix=False):
        """Check if request matchs the given parameters.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        path: str
            HTTP path relative to the service.path.
        methods: list
            HTTP methods.
        prefix: bool
            If True it works like str.startswith for path.

        Returns
        -------
        :class:`.Match`
            Match instance.
        """
        match = ExistentMatch()
        if path is not None:
            path = self.service.path + path
            match1 = self.__match_path(request, path, prefix)
            if not match1:
                return NonExistentMatch()
            match = match1
        if methods is not None:
            match2 = self.__match_methods(request, methods)
            if not match2:
                return NonExistentMatch()
        return match

    # Private

    def __add_converters(self):
        self.converters.add(StringConverter(self.service))
        self.converters.add(IntegerConverter(self.service))
        self.converters.add(FloatConverter(self.service))
        self.converters.add(PathConverter(self.service))

    def __match_path(self, request, path, prefix=False):
        if path not in self.__patterns:
            self.__patterns[path] = Pattern.create(path, self.converters)
        pattern = self.__patterns[path]
        match = pattern.match(request.path, prefix=prefix)
        return match

    def __match_methods(self, request, methods):
        match = ExistentMatch()
        if methods is not None:
            methods = map(str.upper, methods)
            if request.method not in methods:
                return NonExistentMatch()
        return match
