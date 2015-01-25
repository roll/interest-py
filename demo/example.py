import sys
import json
import asyncio
import logging
from aiohttp.web import Response, HTTPCreated, HTTPException, HTTPServerError
from interest import Service, Resource, Middleware, get, put


class Responder(Middleware):

    # Public

    @asyncio.coroutine
    def __call__(self, request):
        try:
            response = Response()
            route = yield from self.service.dispatcher.dispatch(request)
            payload = yield from route.responder(request, **route.match)
        except HTTPException as exception:
            response = exception
            payload = {'message': str(response)}
        except Exception as exception:
            response = HTTPServerError()
            payload = {'message': 'Something went wrong!'}
        response.text = json.dumps(payload)
        response.content_type = 'application/json'
        return response


class Comment(Resource):

    # Public

    @get('/<key:int>')
    def read(self, request, *, key):
        return {'key': key}

    @put
    def upsert(self, request):
        raise HTTPCreated()


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
service.add_middleware(Responder)
service.add_resource(Comment)
service.listen(hostname=hostname, port=port)
