import sys
import json
import asyncio
import logging
from interest import Service, Middleware, Resource, http


class Session(Middleware):

    # Public

    @asyncio.coroutine
    def __call__(self, request):
        request.session = True
        response = yield from self.next(request)
        return response


class Restful(Middleware):

    # Public

    @asyncio.coroutine
    def __call__(self, request):
        try:
            response = http.Response()
            route = yield from self.service.dispatcher.dispatch(request)
            payload = yield from route.responder(request, **route.match)
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
        return {'key': key, 'session': request.session}

    @http.put
    def upsert(self, request):
        raise http.Created()


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
