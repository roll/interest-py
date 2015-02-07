# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Features
--------

There are main interest features:

- event-driven on top of aiohttp/asyncio

    Asyncio is fast and beautifull. It's now is a part of Python standard 
    library. Meanwhile aiohttp is probably going to be standard HTTP 
    binding for asyncio. Interest is compatible with 
    aiohttp's Request/Response/middleware. 

- consistent, modular and flexible flow model, class-based

    In interest everything processing request is a middleware. It's more 
    like express.js/koa.js than aiohttp.web. As opposed to js libraries 
    here we can write on beloved Python language instead of beloved 
    Javascript language. Of course there is no callback hell thanks 
    to asyncio. Furthermore Interest is fully class-based. For example 
    endpoint is a middleware method. There are much more interesting 
    things about flow model, see examples and documentation.   

- configurable and pluggable

    Interest is designed to be fully configurable in declarative manner
    without subclassing main components. Interest supports providers 
    and plugins. Virtual plugin repository based on github is a the 
    work in progress.

Package is authored and maintained by {{ maintainer }} <{{ maintainer_email }}>.

Getting ready
-------------

To get started we need Python 3.4+. Installation is simple:

- pip3 install {{ pypi_name }}

Minimal server
--------------

Finally showing you the code:

.. code-block:: python

    {{ examples['server']|indent }}
    
Run the server in the terminal and use another to interact:
    
.. code-block:: bash

    $ python3 server.py
    ...
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World!
  
Adding middlewares
------------------

Now we're adding some middlewares:

.. code-block:: python

    {{ examples['middlewares']|indent }}
    
Run the server in the terminal and use another to interact:
    
.. code-block:: bash

    $ python3 server.py
    ...
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World!
    $ curl -X GET http://127.0.0.1:9000/math/power/2; echo
    4
    $ curl -X GET http://127.0.0.1:9000/math/power/two; echo 
    404: Not Found

Diving into features
--------------------

Now we're creating restful API exploring interest features:

.. code-block:: python

    {{ examples['features']|indent }}
    
Run the server in the terminal and use another to interact:  
    
.. code-block:: bash

    $ python3 server.py
    INFO:interest:Start listening host="127.0.0.1" port="9000"
    ... <see log here> ... 
    $ curl -X GET http://127.0.0.1:9000/api/v1/comment/key=1; echo
    {"key": 1}
    $ curl -X PUT http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Created"}
    $ curl -X POST http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Unauthorized"}

{% endblock %}

{% block requirements %}{% endblock %}
{% block installation %}{% endblock %}
{% block contribution %}{% endblock %}
