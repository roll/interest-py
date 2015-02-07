# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Main features
-------------

Getting ready
-------------

Minimal server
--------------

Base example of the interest:

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
