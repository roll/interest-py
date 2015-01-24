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
    from aiohttp.web import Response, HTTPCreated, HTTPException, HTTPServerError
    from interest import Service, Resource, Middleware, get, put
    
    
    class Interface(Middleware):
    
        # Public
    
        @asyncio.coroutine
        def __call__(self, request):
            try:
                response = Response()
                payload = yield from self.next(request)
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
    
        @get('/<id:int>')
        def read(self, request):
            return {'id': request.route['id']}
    
        @put
        def upsert(self, request):
            raise HTTPCreated()
  
    
    logging.basicConfig(level=logging.INFO)
    service = Service(path='/api/v1')
    service.add_resource(Comment)
    service.add_middleware(Interface)
    service.listen(hostname='127.0.0.1', port=9000)
    
- run the server using python3 interpreter:

  .. code-block:: bash

    $ python3 server.py
    INFO:interest:Start listening at http://127.0.0.1:9000
    ... <see log here> ... 
    
- open a new terminal window and make a request:

  .. code-block:: bash

    $ curl -X GET http://127.0.0.1:9000/api/v1/comment/1; echo
    {"id": 1}
    $ curl -X PUT http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Created"}

{% endblock %}