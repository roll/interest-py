import asyncio
from abc import ABCMeta


class Middleware(metaclass=ABCMeta):

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
        return self.__service
