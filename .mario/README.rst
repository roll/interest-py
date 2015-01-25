# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Example
-------

Here is a base usage example.

- create server.py in current working directory:

  .. code-block:: python

    import json
    import asyncio
    import logging
    from interest import Service, Middleware, Resource, http
    
    
    class Session(Middleware):
    
        # Public
    
        @asyncio.coroutine
        def __call__(self, request):
            request.session = 'session'
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
            return {'key': key}
    
        @http.put
        def upsert(self, request):
            raise http.Created()
    
    
    logging.basicConfig(level=logging.DEBUG)
    service = Service(path='/api/v1')
    service.add_middleware(Session)
    service.add_middleware(Restful)
    service.add_resource(Comment)
    service.listen(hostname='127.0.0.1', port=9000)
    
- run the server using python3 interpreter:

  .. code-block:: bash

    $ python3 server.py
    INFO:interest:Start listening at http://127.0.0.1:9000
    ... <see log here> ... 
    
- open a new terminal window and make a request:

  .. code-block:: bash

    $ curl -X GET http://127.0.0.1:9000/api/v1/comment/1; echo
    {"key": 1}
    $ curl -X PUT http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Created"}

{% endblock %}