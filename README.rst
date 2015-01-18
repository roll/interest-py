.. Block: caution

.. TO MAKE CHANGES USE [meta] DIRECTORY.

.. Block: description

Interest
=====================
Interest is a REST framework on top of aiohttp/asyncio (experimental).

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

    import logging
    from aiohttp.web import Response, HTTPCreated
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
    
        def process_data(self, data):
            response = Response(
                text=self.service.formatter.encode(data),
                content_type=self.service.formatter.content_type)
            return response
    
        def process_exception(self, exception):
            data = {'message': str(exception)}
            exception.text = self.service.formatter.encode(data)
            exception.content_type = self.service.formatter.content_type
            return exception
  
    
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

Copyright (c) 2014 Respect31 <post@respect31.com>

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
