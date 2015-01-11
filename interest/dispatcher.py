import asyncio
from aiohttp.web import UrlDispatcher, HTTPException
from .match import ExistentMatch, NonExistentMatch
from .resource import Resource


class Dispatcher:

    # Public

    def __init__(self, service):
        self.__service = service
        self.__resources = []

    @property
    def service(self):
        return self.__service

    @property
    def resources(self):
        return self.__resources

    def add_resource(self, *resources, source=None):
        for resource in resources:
            resource = resource(self.service)
            self.resources.append(resource)
        if source is not None:
            for resource in vars(source).values():
                if isinstance(resource, type):
                    if issubclass(resource, Resource):
                        self.add_resource(resource)

    @asyncio.coroutine
    def resolve(self, request):
        router = self.__make_router()
        try:
            match_info = yield from router.resolve(request)
            match = ExistentMatch(match_info.route, groups=match_info)
        except HTTPException as exception:
            match = NonExistentMatch(exception)
        return match

    # Private

    def __make_router(self):
        router = UrlDispatcher()
        for resource in self.resources:
            for binding in resource.bindings:
                binding.register(
                    service=self.service,
                    resource=resource,
                    router=router)
        return router
