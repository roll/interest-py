import sys
import logging
from aiohttp.web import Response, HTTPCreated
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

    def process_data(self, data):
        response = Response(
            text=self.service.formatter.encode(data),
            content_type=self.service.formatter.content_type)
        return response

    def process_exception(self, exception):
        data = {'message': str(exception)}
        exception.text = self.service.formatter.encode(data)
        exception.content_type = self.service.formatter.content_type
        return exception


hostname = '127.0.0.1'
try:
    port = int(sys.argv[1])
except Exception:
    port = 9000

logging.basicConfig(level=logging.DEBUG)
service = Service(path='/api/v1')
service.add_resource(Comment)
service.add_middleware(Interface)
service.listen(hostname=hostname, port=port)
