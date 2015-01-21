import asyncio
from abc import ABCMeta


class Middleware(metaclass=ABCMeta):
    """Middleware representation.

    Middlewares is used by :class:`.Processor` to process request,
    data, response and exception. Middleware **CAN** have process_*
    hooks which will be used by processor. Those methods **CAN**
    be or not to be coroutins. See hooks list below.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Hooks
    -----
    process_request(request)
        Process request.
    process_data(request, data)
        Process data.
    process_response(request, response)
        Process response.
    process_exception(request, exception)
        Process exception.

    Example
    -------
    By default interest doesn't know what to do with data returned
    by responder. We have to implement convertation midleware::

        class ConvertationMiddleware(Middleware):

            # Public

            def process_data(self, request, data):
                response = Response(
                    text=self.service.formatter.encode(data),
                    content_type=self.service.formatter.content_type)
                return response

        service = Service(path='/api/v1')
        service.add_middleware(ConvertationMiddleware)
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
