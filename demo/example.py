import logging
from aiohttp.web import Response, HTTPClientError, HTTPServerError
from interest import Service, Resource, Middleware, get


class Comment(Resource):

    # Public

    @get('/{id}')
    def read(self, request):
        return {'action': 'read'}


class Interface(Middleware):

    # Public

    def process_data(self, data):
        response = Response(
            text=self.service.formatter.encode(data),
            content_type=self.service.formatter.content_type)
        return response

    def process_exception(self, exception):
        if isinstance(exception, (HTTPClientError, HTTPServerError)):
            data = {'error': str(exception)}
            exception.text = self.service.formatter.encode(data)
            exception.content_type = self.service.formatter.content_type
        return exception


logging.basicConfig(level=logging.INFO)
service = Service(path='/api/v1')
service.add_resource(Comment)
service.add_middleware(Interface)
service.listen(hostname='127.0.0.1', port=9000)
