.. Block: caution

.. TO MAKE CHANGES USE [meta] DIRECTORY.

.. Block: description

Interest
=====================
Interest is a REST framework on top of aiohttp/asyncio.

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


Minimal service
---------------

.. code-block:: python

  import sys
    from interest import Service, http
    
    
    class Service(Service):
    
        # Public
    
        @http.get('/<key:path>')
        def hello(self, request, key):
            return http.Response(text='Hello World!')
    
    
    # Create server
    service = Service()
    
    # Listen forever
    argv = dict(enumerate(sys.argv))
    service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))
  
Adding middlewares
------------------

.. code-block:: python

  import sys
    import asyncio
    from interest import Service, Middleware, http
    
    
    class Processor(Middleware):
    
        # Public
    
        @asyncio.coroutine
        def process(self, request):
            try:
                # Process request here
                response = (yield from self.next(request))
                # Process response here
            except http.Exception as exception:
                # Process exception here
                response = exception
            return response
    
    
    class Resource(Middleware):
    
        # Public
    
        @http.get('/<key:path>')
        def hello(self, request, key):
            return http.Response(text='Hello World!')
    
    
    # Create server
    service = Service(
        middlewares=[Processor, Resource])
    
    # Listen forever
    argv = dict(enumerate(sys.argv))
    service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))

Diving into features
--------------------

Create server.py in current working directory:

.. code-block:: python

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
    
    
    class Comment(Middleware):
    
        # Public
    
        PREFIX = '/comment'
        MIDDLEWARES = [Auth]
    
        @http.get('/key=<key:int>')
        def read(self, request, key):
            url = '/api/v1/comment/key=' + str(key)
            assert url == self.service.url('comment.read', key=key)
            assert url == self.service.url('read', base=self, key=key)
            return {'key': key}
    
        @http.put
        @http.post  # Endpoint's behind the Auth
        def upsert(self, request):
            self.service.log('info', 'Adding custom header!')
            raise http.Created(headers={'endpoint': 'upsert'})
    
    
    # Create restful service
    restful = Service(
        prefix='/api/v1',
        middlewares=[Restful, Session, Comment])
    
    # Create main service
    service = Service(
        logger=Logger.config(
            template='%(request)s | %(status)s | %(<endpoint:res>)s'),
        handler=Handler.config(
            connection_timeout=25, request_timeout=5))
    
    # Add restful to main
    service.push(restful)
    
    # Listen forever
    argv = dict(enumerate(sys.argv))
    logging.basicConfig(level=logging.DEBUG)
    service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))
    
Run the server using python3 interpreter:

.. code-block:: bash

  $ python3 server.py
  INFO:interest:Start listening host="127.0.0.1" port="9000"
  ... <see log here> ... 
    
Open a new terminal window and make some requests:

.. code-block:: bash

  $ curl -X GET http://127.0.0.1:9000/api/v1/comment/key=1; echo
  {"key": 1}
  $ curl -X PUT http://127.0.0.1:9000/api/v1/comment; echo
  {"message": "Created"}
  $ curl -X POST http://127.0.0.1:9000/api/v1/comment; echo
  {"message": "Unauthorized"}


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
- pip3 install interest

.. Block: contribution

Contribution
------------
- Authors

  - roll <roll@respect31.com>
- Maintainers

  - roll <roll@respect31.com>

.. Block: stability

Stability
---------
Package's `public API  <http://interest.readthedocs.org/en/latest/reference.html>`_
follows `semver <http://semver.org/>`_ versioning model:

- DEVELOP: 0.X[Breaking changes][API changes].X[Minor changes]
- PRODUCT: X[Breaking changes].X[API changes].X[Minor changes]

Be careful on DEVELOP stage package is under active development
and can be drastically changed or even deleted. Don't use package
in production before PRODUCT stage is reached.

For the more information see package's 
`changelog  <http://interest.readthedocs.org/en/latest/changes.html>`_.

.. Block: license

License
-------
**MIT License**

© Copyright 2015, Respect31.

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
