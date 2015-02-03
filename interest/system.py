import asyncio
from abc import ABCMeta, abstractmethod
from .middleware import Middleware


class SystemMiddleware(Middleware, metaclass=ABCMeta):
    """Adapter for aiohttp.web midleware factories.
    """

    # Public

    # TODO: rename to factory?
    @property
    @abstractmethod
    def system(self):
        pass  # pragma: no cover

    @asyncio.coroutine
    def __call__(self, request):
        handler = yield from self.system(None, self.next)
        return (yield from handler(request))
