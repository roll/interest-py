# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Example
-------

Here is a base usage example.

- create server.py in current working directory:

  .. code-block:: python

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
    {"id": "1"}
    $ curl -X PUT http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Created"}

{% endblock %}