import sys
import asyncio
import logging
from aiohttp.web import Response, HTTPException, HTTPCreated
from interest import Service, Resource, Middleware, get, put


class Comment(Resource):

    # Public

    @get('/{id}')
    def read(self, request):
        return {'id': request.match['id']}

    @put
    def upsert(self, request):
        raise HTTPCreated()


class Interface(Middleware):

    # Public

    @asyncio.coroutine
    def process_data(self, request, data):
        response = Response(
            text=self.service.formatter.encode(data),
            content_type=self.service.formatter.content_type)
        return response

    @asyncio.coroutine
    def process_response(self, request, response):
        if isinstance(response, HTTPException):
            data = {'message': str(response)}
            response.text = self.service.formatter.encode(data)
            response.content_type = self.service.formatter.content_type
        return response


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
service.add_resource(Comment)
service.add_middleware(Interface)
service.listen(hostname=hostname, port=port)
