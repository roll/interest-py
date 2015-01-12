# Forked from aiohttp.web
# TODO: it needs refactoring/simplification to meet interest requirements
import re
import asyncio
from aiohttp.web import HTTPNotFound, HTTPMethodNotAllowed
from .route import DynamicRoute, PlainRoute


class UrlDispatcher:

    # Public

    DYN = re.compile(r'^\{(?P<var>[a-zA-Z][_a-zA-Z0-9]*)\}$')
    DYN_WITH_RE = re.compile(
        r'^\{(?P<var>[a-zA-Z][_a-zA-Z0-9]*):(?P<re>.+)\}$')
    GOOD = r'[^{}/]+'
    PLAIN = re.compile('^' + GOOD + '$')
    METHODS = {'POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}

    def __init__(self):
        super().__init__()
        self._urls = []
        self._routes = {}

    @asyncio.coroutine
    def resolve(self, request):
        path = request.path
        method = request.method
        allowed_methods = set()
        for route in self._urls:
            match_dict = route.match(path)
            if match_dict is None:
                continue
            route_method = route.method
            if route_method != method:
                allowed_methods.add(route_method)
            else:
                return UrlMappingMatchInfo(match_dict, route)
        else:
            if allowed_methods:
                raise HTTPMethodNotAllowed(method, allowed_methods)
            else:
                raise HTTPNotFound()

    def add_route(self, method, path, handler, *, name=None):
        assert path.startswith('/')
        assert callable(handler), handler
        if not asyncio.iscoroutinefunction(handler):
            handler = asyncio.coroutine(handler)
        method = method.upper()
        assert method in self.METHODS, method
        parts = []
        factory = PlainRoute
        for part in path.split('/'):
            if not part:
                continue
            match = self.DYN.match(part)
            if match:
                parts.append('(?P<' + match.group('var') + '>' +
                             self.GOOD + ')')
                factory = DynamicRoute
                continue

            match = self.DYN_WITH_RE.match(part)
            if match:
                parts.append('(?P<' + match.group('var') + '>' +
                             match.group('re') + ')')
                factory = DynamicRoute
                continue
            if self.PLAIN.match(part):
                parts.append(re.escape(part))
                continue
            raise ValueError("Invalid path '{}'['{}']".format(path, part))
        if factory is PlainRoute:
            route = PlainRoute(method, handler, name, path)
        else:
            pattern = '/' + '/'.join(parts)
            if path.endswith('/') and pattern != '/':
                pattern += '/'
            try:
                compiled = re.compile('^' + pattern + '$')
            except re.error as exc:
                raise ValueError(
                    "Bad pattern '{}': {}".format(pattern, exc)) from None
            route = DynamicRoute(method, handler, name, compiled, path)
        self._register_endpoint(route)
        return route

    # Protected

    def _register_endpoint(self, route):
        name = route.name
        if name is not None:
            if name in self._routes:
                raise ValueError('Duplicate {!r}, '
                                 'already handled by {!r}'
                                 .format(name, self._routes[name]))
            else:
                self._routes[name] = route
        self._urls.append(route)


class UrlMappingMatchInfo(dict):

    # Public

    def __init__(self, match_dict, route):
        super().__init__(match_dict)
        self._route = route

    @property
    def handler(self):
        return self._route.handler

    @property
    def route(self):
        return self._route
