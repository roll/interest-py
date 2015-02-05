import asyncio
from .helpers import Config


class Provider(Config):
    """Provider representation (abstract).
    """

    # Public

    PROVIDE = None

    def __init__(self, service, *, provide=None):
        if provide is None:
            provide = self.PROVIDE
        assert provide is not None
        self.__service = service
        self.__provide = provide

    def __repr__(self):
        template = '<Provider provide="{self.provide}">'
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @asyncio.coroutine
    def provide(self):
        return (yield from self.__provide())
