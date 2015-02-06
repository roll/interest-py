# middlewares.py
import sys
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

    @http.get('/<key:path>')
    def hello(self, request, key):
        return http.Response(text='Hello World!')


# Create server
service = Service(middlewares=[Processor, Resource])

# Listen forever
argv = dict(enumerate(sys.argv))
service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))
