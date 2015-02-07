# server.py
import asyncio
from interest import Service, Middleware, http


class Processor(Middleware):

    # Public

    @asyncio.coroutine
    def process(self, request):
        try:
            # Process request here
            response = (yield from self.next(request))
            # Process response here
        except http.Exception as exception:
            # Process exception here
            response = exception
        return response


class Resource(Middleware):

    # Public

    PREFIX = '/math'

    @http.get('/power')
    @http.get('/power/<value:int>')
    def power(self, request, value=1):
        return http.Response(text=str(value ** 2))


class Service(Service):

    # Public

    @http.get('/')
    def hello(self, request, key):
        return http.Response(text='Hello World!')


# Listen forever
service = Service(middlewares=[Processor, Resource])
service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
