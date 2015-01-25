.. Block: caution

.. TO MAKE CHANGES USE [meta] DIRECTORY.

.. Block: description

Interest
=====================
Interest is a web framework on top of asyncio and aiohttp.

.. Block: badges

.. image:: http://img.shields.io/badge/code-GitHub-brightgreen.svg
     :target: https://github.com/interest-hub/interest
     :alt: code
.. image:: http://img.shields.io/travis/interest-hub/interest/master.svg
     :target: https://travis-ci.org/interest-hub/interest 
     :alt: build
.. image:: http://img.shields.io/coveralls/interest-hub/interest/master.svg 
     :target: https://coveralls.io/r/interest-hub/interest  
     :alt: coverage
.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg
     :target: http://interest.readthedocs.org
     :alt: docs     
.. image:: http://img.shields.io/pypi/v/interest.svg
     :target: https://pypi.python.org/pypi?:action=display&name=interest
     :alt: pypi


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
                route = yield from self.service.dispatcher.dispatch(request)
                payload = yield from route.responder(request, **route.match)
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
    
        @get('/<key:int>')
        def read(self, request, *, key):
            return {'key': key}
    
        @put
        def upsert(self, request):
            raise HTTPCreated()
  
    
    logging.basicConfig(level=logging.INFO)
    service = Service(path='/api/v1')
    service.add_middleware(Interface)
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


.. Block: application

Application
-----------
Package is under active development and is not ready for production use.
Backward-compatibility between minor releases (0.x.0), documentation and 
changelog are not guaranteed to be present before stable versions (>=1.0.0).

.. Block: requirements

Requirements
------------
- Platforms

  - Unix
- Interpreters

  - Python 3.4

.. Block: installation

Installation
------------
- pip install interest

.. Block: contribution

Contribution
------------
- Authors

  - roll <roll@respect31.com>
- Maintainers

  - roll <roll@respect31.com>

.. Block: changelog

Changelog
---------
- no entries yet

.. Block: license

License
-------
**MIT License**

Copyright (c) 2015 Respect31 <post@respect31.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
