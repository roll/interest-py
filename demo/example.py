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

    def process_data(self, request, data):
        formatter = request.service.formatter
        text = formatter.encode(data)
        response = Response(text=text, content_type=formatter.content_type)
        return response

    def process_exception(self, exception):
        formatter = exception.request.service.formatter
        if isinstance(exception, (HTTPClientError, HTTPServerError)):
            exception.content_type = formatter.content_type
            exception.text = formatter.encode({'error': str(exception)})
        return exception


logging.basicConfig(level=logging.INFO)
service = Service(path='/api/v1')
service.add_resource(Comment)
service.add_middleware(Interface)
service.listen(hostname='127.0.0.1', port=9000)
