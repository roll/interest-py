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

    @http.get('/')
    @http.get('/<times:int>')
    def hello(self, request, times=1):
        return http.Response(text='Hello World {} times!'.format(times))


# Listen forever
service = Service(middlewares=[Processor, Resource])
service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
