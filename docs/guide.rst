Extended Guide
==============

Welcome to the interest's extended guide. We will try to cover all 
framework aspects. If you're interested in concrete topic use left 
menu to pick it.   

*under development*

Terminology
-----------
    
Flow model
----------

Routing
-------

Logging
-------

Testing
-------

Debugging
---------

Serving static
--------------

Template engines
----------------

Database integration
--------------------

Putting all together
--------------------

We'll put all features together to the example: 

.. literalinclude:: ../demo/advanced.py

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
