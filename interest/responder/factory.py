import asyncio
from abc import ABCMeta, abstractmethod
from .middleware import Middleware


class FactoryMiddleware(Middleware, metaclass=ABCMeta):
    """Adapter for aiohttp.web midleware factories.
    """

    # Public

    @property
    @abstractmethod
    def factory(self):
        pass  # pragma: no cover

    @asyncio.coroutine
    def __call__(self, request):
        handler = self.factory(None, self.next)
        return (yield from handler(request))
