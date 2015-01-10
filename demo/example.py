import logging
from interest import Service, Resource, Middleware, get


class Auth(Middleware):

    # Public

    def process_request(self, request):
        request.hello = True
        return request


class Comment(Resource):

    # Public

    @get('/{id}')
    def read(self, request):
        return {'hello': request.hello}


logging.basicConfig(level=logging.INFO)
service = Service(path='/api/v1')
service.add_middleware(Auth)
service.add_resource(Comment)
service.listen(hostname='127.0.0.1', port=9000)
