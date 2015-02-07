import asyncio
from .middleware import Middleware


class Adapter(Middleware):
    """Adapter is a middleware to use aiohttp.web's middleware factories.

    .. seealso:: Implements:
        :class:`.Middleware`
        :class:`.Chain`,
        :class:`.Config`

    Parameters
    ----------
    factory: coroutine
        aiohttp.web's middleware factoriy.
    """

    # Public

    def __init__(self, *args, factory, **kwargs):
        self.__factory = factory
        super.__init__(*args, **kwargs)

    @asyncio.coroutine
    def process(self, request):
        handler = yield from self.factory(None, self.next)
        return (yield from handler(request))
