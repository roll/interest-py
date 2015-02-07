import asyncio
from .helpers import Config


class Provider(Config):
    """Provider is a extended coroutine to update the service.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    provide: coroutine
        Coroutine for actual work.
    """

    # Public

    PROVIDE = None
    """Default provide parameter.
    """

    def __init__(self, service, *, provide=None):
        if provide is None:
            provide = self.PROVIDE
        self.__service = service
        # Override attributes
        if provide is not None:
            self.provide = provide

    @asyncio.coroutine
    def __call__(self, service):
        """Update the service.

        Parameters
        ----------
        service: :class:`.Service`
            Service instance.
        """
        return (yield from self.provide(service))

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
    def provide(self, service):
        """Update the service.

        Parameters
        ----------
        service: :class:`.Service`
            Service instance.
        """
        raise NotImplementedError()
