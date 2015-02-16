.. Block: caution

.. TO MAKE CHANGES USE [.mario] DIRECTORY.

.. Block: description

Interest
=====================
Interest is a event-driven web framework on top of aiohttp/asyncio.

.. image:: http://img.shields.io/badge/code-github-brightgreen.svg
     :target: https://github.com/inventive-ninja/interest
     :alt: code
.. image:: http://img.shields.io/badge/board-kanban-brightgreen.svg
     :target: https://waffle.io/inventive-ninja/interest
     :alt: board
.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg
     :target: http://interest.readthedocs.org
     :alt: docs
.. image:: http://img.shields.io/badge/chat-online-brightgreen.svg
     :target: https://gitter.im/inventive-ninja/public
     :alt: chat
.. image:: http://img.shields.io/badge/groups-public-brightgreen.svg
     :target: https://groups.google.com/forum/#!forum/inventive-ninja
     :alt: groups 
.. image:: http://img.shields.io/badge/questions-soon-yellow.svg
     :target: http://stackoverflow.com/
     :alt: questions  

----
        
.. image:: http://img.shields.io/pypi/v/interest.svg
     :target: https://pypi.python.org/pypi?:action=display&name=interest
     :alt: pypi
.. image:: http://img.shields.io/travis/inventive-ninja/interest/master.svg
     :target: https://travis-ci.org/inventive-ninja/interest 
     :alt: build
.. image:: http://img.shields.io/coveralls/inventive-ninja/interest/master.svg 
     :target: https://coveralls.io/r/inventive-ninja/interest  
     :alt: coverage
               
Features
--------

- event-driven on top of aiohttp/asyncio

    Asyncio is a asynchronous library. Fast and beautifull. It's now 
    is a part of the Python. Meanwhile aiohttp is probably going to 
    be standard HTTP binding for asyncio. Interest is compatible with 
    aiohttp's Request/Response/middleware. 

- consistent, modular and flexible flow model, class-based

    In interest everything processing request is a middleware. It's more 
    like express.js/koa.js than aiohttp.web. Furthermore Interest is 
    fully class-based. For example endpoint is a middleware's method. 
    There are much more interesting things about flow model, 
    see examples and documentation.   

- configurable and pluggable

    Interest is designed to be fully configurable in declarative manner
    without subclassing main components. Interest supports providers 
    and plugins. Virtual plugin repository based on github is a
    work in progress.

Package is authored and maintained by roll <roll@respect31.com>.

Installation
------------

We need Python 3.4+ and higher:

- pip3 install interest

Creating service
----------------

Service is a main interest component. Service can listen on TCP/IP port.
It means that when we create service and call listen method we create
HTTP server:

.. code-block:: python

    # server.py
    from interest import Service, http
    
    
    class Service(Service):
    
        # Public
    
        @http.get('/')
        def hello(self, request):
            return http.Response(text='Hello World!')
    
    
    # Listen forever
    service = Service()
    service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
    
Run the server in the terminal and use another to interact:
    
.. code-block:: bash

    $ python3 server.py
    ...
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World!
  
Adding middlewares
------------------

As it was said service is a main interest component but heart of the interest 
is a middleware concept. For example service is also a middleware.  

  Middleware is a coroutine taking http.Request as first argument 
  to return any object.
  
Interest provides class-based middleware with extended API.
For example you can set constraints like HTTP path or methods, 
call the next middleware, get access to the parent service and more:

.. code-block:: python

    # server.py
    import asyncio
    from interest import Service, Middleware, http
    
    
    class Upper(Middleware):
    
        # Public
    
        PREFIX = '/upper'
        METHODS = ['GET']
    
        @asyncio.coroutine
        def process(self, request):
            try:
                # Process request here
                response = (yield from self.next(request))
                # Process response here
                response.text = response.text.upper()
            except http.Exception as exception:
                # Process exception here
                response = exception
            print(self.service)
            return response
    
    
    class Service(Service):
    
        # Public
    
        @http.get('/<key:path>')
        def hello(self, request, key):
            return http.Response(text='Hello World!')
    
    
    # Listen forever
    service = Service(middlewares=[Upper])
    service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
    
Run the server in the terminal and use another to interact:
    
.. code-block:: bash

    $ python3 server.py
    ...
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World!
    $ curl -X GET http://127.0.0.1:9000/upper/; echo
    HELLO WORLD!

Adding endpoints
----------------

Endpoint is a middleware responsible for responding to a request.
To create endpoint you just wrap middleware's method by one or a few http.bind 
functions. We already saw it in a very first example. Add some endpoints: 

.. code-block:: python

  # server.py
    import asyncio
    from interest import Service, Middleware, http
    
    
    class Math(Middleware):
    
        # Public
    
        PREFIX = '/math'
    
        @http.get('/power')
        @http.get('/power/<value:int>')
        def power(self, request, value=1):
            return http.Response(text=str(value ** 2))
    
    
    class Upper(Middleware):
    
        # Public
    
        PREFIX = '/upper'
        METHODS = ['GET']
    
        @asyncio.coroutine
        def process(self, request):
            try:
                # Process request here
                response = (yield from self.next(request))
                # Process response here
                response.text = response.text.upper()
            except http.Exception as exception:
                # Process exception here
                response = exception
            print(self.service)
            return response
    
    
    class Service(Service):
    
        # Public
    
        @http.get('/<key:path>')
        def hello(self, request, key):
            return http.Response(text='Hello World!')
    
    
    # Listen forever
    service = Service(middlewares=[Math, Upper])
    service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
  
Run the server in the terminal and use another to interact:
    
.. code-block:: bash

    $ python3 server.py
    ...
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World!
    $ curl -X GET http://127.0.0.1:9000/upper/; echo
    HELLO WORLD!    
    $ curl -X GET http://127.0.0.1:9000/math/power/2; echo
    4
    $ curl -X GET http://127.0.0.1:9000/math/power/two; echo 
    404: Not Found
    
What's next?
------------

See the Interest documentation to get more:

  It's under development for now.

- `Getting started <http://interest.readthedocs.org/en/latest/tutorial.html>`_
- `Extended Guide <http://interest.readthedocs.org/en/latest/guide.html>`_
- `API Reference <http://interest.readthedocs.org/en/latest/reference.html>`_
- `Questions <http://interest.readthedocs.org/en/latest/questions.html>`_
- `Changes <http://interest.readthedocs.org/en/latest/changes.html>`_





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

© Copyright 2015, Inventive Ninja.

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
