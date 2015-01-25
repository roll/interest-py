import asyncio
from aiohttp.web import HTTPNotFound, HTTPMethodNotAllowed
from ..helpers import Chain
from .pattern import Pattern
from .route import ExistentRoute, NonExistentRoute
from .converter import (FloatConverter, IntegerConverter,
                        PathConverter, StringConverter)

class Dispatcher:
    """Dispatcher representation.
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
        """List of resources.
        """
        return self.__resources

    @property
    def converters(self):
        """Dict of converters.
        """
        return self.__converters

    @asyncio.coroutine
    def dispatch(self, request):
        route = NonExistentRoute(HTTPNotFound())
        # Check the service
        path = self.service.path
        match = self.__match_path(request, path, prefix=True)
        if match is None:
            return route
        # Check the resources
        match = None
        for resource in self.resources:
            path = self.service.path + resource.path
            match = self.__match_path(request, path, prefix=True)
            if match is not None:
                break
        if match is None:
            return route
        # Check the bingings
        for binding in resource.bindings:
            path = self.service.path + resource.path + binding.path
            match1 = self.__match_path(request, path)
            if match1 is None:
                continue
            match2 = self.__match_methods(request, binding.methods)
            if match2 is None:
                return NonExistentRoute(
                    HTTPMethodNotAllowed(request.method, binding.methods))
            return ExistentRoute(binding.responder, match1)
        return route

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
        match = {}
        if methods is not None:
            methods = map(str.upper, methods)
            if request.method not in methods:
                return None
        return match
