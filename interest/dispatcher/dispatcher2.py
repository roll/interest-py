from aiohttp.web import HTTPNotFound, HTTPMethodNotAllowed
from ..helpers import FeedbackList
from .match import NonExistentMatch


class Dispatcher:
    """Dispatcher representation.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__resources = FeedbackList(
            self.__on_resources_change)
        self.__patterns = {}

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def resources(self):
        """List of middlewares.
        """
        return self.__resources

    def dispatch(self, request):
        # Check the service
        match = self.resolve(request)
        if not match:
            return match
        # Check the resources
        resource = None
        match = NonExistentMatch(HTTPNotFound())
        for resource in self.resources:
            match = self.resolve(request, path=resource.path)
            if match:
                break
        if not match:
            return match
        # Check the bingings
        match = NonExistentMatch(HTTPNotFound())
        for binding in resource:
            match = self.resolve(
                request, path=binding.path, methods=binding.methods)
            if match:
                break
        return match

    def resolve(self, request, *, path=None, methods=None):
        """Resolve a request for the given path and methods.
        """
        # Check the service path
        if not request.path.startswith(self.service.path):
            exception = HTTPNotFound()
            return NonExistentMatch(exception)
        # Check allowed methods
        if methods is not None:
            methods = map(str.upper, methods)
            if request.method not in methods:
                exception = HTTPMethodNotAllowed(request.method, methods)
                return NonExistentMatch(exception)
        # Check the given path
        if path is not None:
            pattern = self.__get_pattern(path)

    # Private

    def __get_pattern(self, path):
        if path not in self.__patterns:
            pattern = self.__compile_pattern(path)
            self.__patterns[path] = pattern
        return self.__patterns[path]

    def __compile_pattern(self, path):
        pass
