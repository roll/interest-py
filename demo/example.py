import sys
import json
import asyncio
import logging
from interest import Service, Middleware, Resource, http


class Session(Middleware):

    # Public

    @asyncio.coroutine
    def __call__(self, request):
        request.user = True
        response = yield from self.next(request)
        return response


class Restful(Middleware):

    # Public

    @asyncio.coroutine
    def __call__(self, request):
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
        raise http.HTTPUnauthorized()


try:
    hostname = sys.argv[1]
except Exception:
    hostname = '127.0.0.1'
try:
    port = int(sys.argv[2])
except Exception:
    port = 9000

logging.basicConfig(level=logging.DEBUG)
service = Service(path='/api/v1')
service.add_middleware(Session)
service.add_middleware(Restful)
service.add_resource(Comment)
service.listen(hostname=hostname, port=port)
