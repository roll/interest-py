# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Minimal service
---------------

Base example of the interest:

.. code-block:: python

    {{ examples['service']|indent }}
    
.. code-block:: bash

    $ python3 server.py
    INFO:interest:Start listening host="127.0.0.1" port="9000"
    ... <see log here> ... 
    $ [NEW TERMINAL]
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World!
  
Adding middlewares
------------------

Now we're adding some middlewares:

.. code-block:: python

    {{ examples['middlewares']|indent }}
    
.. code-block:: bash

    $ python3 server.py
    INFO:interest:Start listening host="127.0.0.1" port="9000"
    ... <see log here> ... 
    $ [NEW TERMINAL]
    $ curl -X GET http://127.0.0.1:9000/; echo
    Hello World 1 times!
    $ curl -X GET http://127.0.0.1:9000/5; echo
    Hello World 5 times!
    $ curl -X GET http://127.0.0.1:9000/ten; echo 
    404: Not Found

Diving into features
--------------------

Now we're creating restful API:

.. code-block:: python

    {{ examples['features']|indent }}
    
.. code-block:: bash

    $ python3 server.py
    INFO:interest:Start listening host="127.0.0.1" port="9000"
    ... <see log here> ... 
    $ [NEW TERMINAL]
    $ curl -X GET http://127.0.0.1:9000/api/v1/comment/key=1; echo
    {"key": 1}
    $ curl -X PUT http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Created"}
    $ curl -X POST http://127.0.0.1:9000/api/v1/comment; echo
    {"message": "Unauthorized"}

{% endblock %}
