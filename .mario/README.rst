# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Minimal service
---------------

.. code-block:: python

  {{ examples['service']|indent }}
  
Adding middlewares
------------------

.. code-block:: python

  {{ examples['middlewares']|indent }}

Diving into features
--------------------

Create server.py in current working directory:

.. code-block:: python

  {{ examples['features']|indent }}
    
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

{% endblock %}