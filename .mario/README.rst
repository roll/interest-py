# REPLACE: README.rst
{% extends 'mario.origin/README.rst' %}

{% block badges %}
{{ super() }}

Example
-------

Here is a base usage example.

- create server.py in current working directory:

  .. code-block:: python

    {{ example|indent }}
    
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

{% endblock %}