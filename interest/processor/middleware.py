from abc import ABCMeta


class Middleware(metaclass=ABCMeta):
    """Middleware representation.

    Middlewares is used by :class:`.Processor` to process request,
    data, response and exception. Middleware **MAY** have process_*
    hooks which will be used by processor. Those methods **MUST**
    be coroutins. See hooks list below.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Hooks
    -----
    process_request(request)
        Process request (coroutine).
    process_data(request, data)
        Process data (coroutine).
    process_response(request, response)
        Process response (coroutine).
    process_exception(request, exception)
        Process exception (coroutine).

    Example
    -------
    By default interest doesn't know what to do with data returned
    by responder. We have to implement convertation midleware::

        class ConvertationMiddleware(Middleware):

            # Public

            @asyncio.coroutine
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

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service
