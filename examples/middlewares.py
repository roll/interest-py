# server.py
import asyncio
from interest import Service, Middleware, http


class Upper(Middleware):

    # Public

    PREFIX = '/upper'
    METHODS = ['GET']

    @asyncio.coroutine
    def process(self, request):
        try:
            # Process request here
            response = (yield from self.next(request))
            # Process response here
            response.text = response.text.upper()
        except http.Exception as exception:
            # Process exception here
            response = exception
        print(self.service)
        return response


class Service(Service):

    # Public

    @http.get('/<key:path>')
    def hello(self, request, key):
        return http.Response(text='Hello World!')


# Listen forever
service = Service(middlewares=[Upper])
service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
