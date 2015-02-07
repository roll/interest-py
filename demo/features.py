# server.py
import json
import asyncio
import logging
from interest import Service, Middleware, http
from interest import Logger, Handler, Router, Parser, Provider, Endpoint


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


class Session(Middleware):

    # Public

    @asyncio.coroutine
    def process(self, request):
        assert self.main == self.service.over
        assert self.over == self.service
        assert self.prev == self.service['restful']
        assert self.next == self.service['comment']
        assert self.next == self.service['comment']['read'].over
        request.user = False
        response = yield from self.next(request)
        return response


class Auth(Middleware):

    # Public

    METHODS = ['POST']

    @asyncio.coroutine
    def process(self, request):
        assert self.service.match(request, root='/api/v1')
        assert self.service.match(request, path=request.path)
        assert self.service.match(request, methods=['POST'])
        if not request.user:
            raise http.Unauthorized()
        response = yield from self.next(request)
        return response


class Endpoint(Endpoint):

    # Public

    HEADERS = []

    def __init__(self, *args, headers=None, **kwargs):
        if headers is None:
            headers = self.HEADERS
        super().__init__(*args, **kwargs)
        self.headers = headers

    @asyncio.coroutine
    def __call__(self, request):
        for header in self.headers:
            if header not in request.headers:
                return (yield from self.next(request))
        return (yield from super().__call__(request))


class Comment(Middleware):

    # Public

    PREFIX = '/comment'
    ENDPOINT = Endpoint
    MIDDLEWARES = [Auth]

    @http.get('/key=<key:myint>')
    def read(self, request, key):
        url = '/api/v1/comment/key=' + str(key)
        assert url == self.service.url('comment.read', key=key)
        assert url == self.service.url('read', base=self, key=key)
        return {'key': key}

    @http.put  # Restful -> Session -> Comment -> upsert
    @http.post  # Restful -> Session -> Comment -> Auth -> upsert
    def upsert(self, request):
        self.service.log('info', 'Adding custom header!')
        raise http.Created(headers={'endpoint': 'upsert'})

    @http.delete(headers=['ACCEPT'])
    def delete(self, request):
        assert self.service.db == '<connection>'
        raise http.Forbidden()


class Database(Provider):

    # Public

    @asyncio.coroutine
    def provide(self, service):
        self.service.db = '<connection>'


# Create restful service
restful = Service(
    prefix='/api/v1',
    middlewares=[Restful, Session, Comment],
    providers=[Database],
    router=Router.config(
        parsers={'myint': Parser.config(
            pattern=r'[1-9]+', convert=int)}))

# Create main service
service = Service(
    logger=Logger.config(
        template='%(request)s | %(status)s | %(<endpoint:res>)s'),
    handler=Handler.config(
        connection_timeout=25, request_timeout=5))

# Add restful to main
service.push(restful)

# Listen forever with logging
logging.basicConfig(level=logging.DEBUG)
service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
