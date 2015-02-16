# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
.. image:: http://img.shields.io/pypi/v/{{ pypi_name }}.svg
     :target: https://pypi.python.org/pypi?:action=display&name={{ pypi_name }}
     :alt: pypi
.. image:: http://img.shields.io/travis/{{ github_user }}/{{ name }}/master.svg
     :target: https://travis-ci.org/{{ github_user }}/{{ name }} 
     :alt: build
.. image:: http://img.shields.io/coveralls/{{ github_user }}/{{ name }}/master.svg 
     :target: https://coveralls.io/r/{{ github_user }}/{{ name }}  
     :alt: coverage

----

.. image:: http://img.shields.io/badge/code-github-brightgreen.svg
     :target: https://github.com/{{ github_user }}/{{ name }}
     :alt: code
.. image:: http://img.shields.io/badge/board-kanban-brightgreen.svg
     :target: https://waffle.io/{{ github_user }}/{{ name }}
     :alt: board
.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg
     :target: http://{{ rtd_name }}.readthedocs.org
     :alt: docs
.. image:: http://img.shields.io/badge/chat-online-brightgreen.svg
     :target: https://gitter.im/{{ github_user }}/public
     :alt: chat
.. image:: http://img.shields.io/badge/groups-public-brightgreen.svg
     :target: https://groups.google.com/forum/#!forum/{{ github_user }}
     :alt: groups 
.. image:: http://img.shields.io/badge/questions-soon-yellow.svg
     :target: http://stackoverflow.com/
     :alt: questions  

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

Package is authored and maintained by {{ maintainer }} <{{ maintainer_email }}>.

Installation
------------

We need Python 3.4+ and higher:

- pip3 install {{ pypi_name }}

Creating service
----------------

Service is a main interest component. Service can listen on TCP/IP port.
It means that when we create service and call listen method we create
HTTP server:

.. code-block:: python

    {{ examples['service']|indent }}
    
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

    {{ examples['middlewares']|indent }}
    
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

  {{ examples['endpoints']|indent }}
  
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

- `Getting started <http://{{ rtd_name }}.readthedocs.org/en/latest/tutorial.html>`_
- `Extended Guide <http://{{ rtd_name }}.readthedocs.org/en/latest/guide.html>`_
- `API Reference <http://{{ rtd_name }}.readthedocs.org/en/latest/reference.html>`_
- `Questions <http://{{ rtd_name }}.readthedocs.org/en/latest/questions.html>`_
- `Changes <http://{{ rtd_name }}.readthedocs.org/en/latest/changes.html>`_

{% endblock %}

{% block requirements %}{% endblock %}
{% block installation %}{% endblock %}
{% block contribution %}{% endblock %}
