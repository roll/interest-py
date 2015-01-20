import asyncio
from abc import ABCMeta


class Middleware(metaclass=ABCMeta):
    """Middleware representation.

    Middlewares is used by :class:`.Processor` to process request,
    data, response and exception. Middleware **CAN** have following
    methods which will be used by processor:

    - process_request(request)
    - process_data(request, data)
    - process_response(request, response)
    - process_exception(request, exception)

    Those methods **CAN** be or not to be coroutins.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        for name in ['process_request',
                     'process_data',
                     'process_response',
                     'process_exception']:
            attr = getattr(self, name, None)
            if attr is not None:
                if not asyncio.iscoroutinefunction(attr):
                    attr = asyncio.coroutine(attr)
                    setattr(self, name, attr)

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service
