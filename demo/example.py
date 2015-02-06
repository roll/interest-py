import sys
import json
import asyncio
import logging
from interest import Service, Middleware, Logger, Handler, http


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
        try:
            request.user = True
            if self.service.match(request, methods=['POST']):
                request.user = False
            response = yield from self.next(request)
        except http.Unauthorized:
            self.service.log('info',
                'It seems like no one can pass '
                'the Auth "%s" middleware. Why?',
                self.service['comment']['auth'])
            raise
        return response


class Auth(Middleware):

    # Public

    METHODS = ['POST']

    @asyncio.coroutine
    def process(self, request):
        if not request.user:
            raise http.Unauthorized()
        response = yield from self.next(request)
        return response


class Comment(Middleware):

    # Public

    PREFIX = '/comment'
    MIDDLEWARES = [Auth]

    @http.get('/key=<key:int>')
    def read(self, request, key):
        return {'next': self.service.url('comment.read', key=key + 1)}

    @http.put  # Endpoint's behind the faith
    @http.post  # Endpoint's behind the Auth
    def upsert(self, request):
        assert self.service.match(
            request,
            root='/api/v1',
            path='/api/v1/comment',
            methods=['PUT', 'POST'])
        raise http.Created(
            headers={'this': self.service.url('upsert', base=self)})


# Create restful service
restful = Service(
    prefix='/api/v1',
    middlewares=[Restful, Session, Comment])

# Create main service
service = Service(
    logger=Logger.config(
        template='%(request)s | %(status)s | %(<this:res>)s'),
    handler=Handler.config(
        connection_timeout=25, request_timeout=5))

# Add restful to main
service.push(restful)

# Listen forever
argv = dict(enumerate(sys.argv))
logging.basicConfig(level=logging.DEBUG)
service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))
