import sys
import json
import asyncio
import logging
from interest import Service, Middleware, Resource, http


class Session(Middleware):

    # Public

    @asyncio.coroutine
    def process(self, request):
        request.user = True
        response = yield from self.next(request)
        return response


class Restful(Middleware):

    # Public

    @asyncio.coroutine
    def process(self, request):
        try:
            response = http.Response()
            payload = yield from self.next(request)
        except http.Exception as exception:
            response = exception
            payload = {'message': str(response)}
        response.text = json.dumps(payload)
        response.content_type = 'application/json'
        return response


class Comment(Resource):

    # Public

    @http.get('/<key:int>')
    def read(self, request, key):
        return {'key': key}

    @http.put
    def upsert(self, request):
        if request.user:
            raise http.Created()
        raise http.Unauthorized()


# Create service
service = Service(path='/api/v1',
    middlewares=[Session, Restful, Comment])

# Listen forever
argv = dict(enumerate(sys.argv))
logging.basicConfig(level=logging.DEBUG)
service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))
