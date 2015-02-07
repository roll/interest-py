Questions
=========

How to start a server manually?
-------------------------------

Just use :meth:`.Service.listen` method without forever flag. 
You can start as many servers on different ports as you want:

.. code-block:: python

    import asyncio
    from interest import Service
    
    service = Service()
    server1 = service.listen(host='127.0.0.1', port=9001) 
    server2 = service.listen(host='127.0.0.1', port=9002)
    try:
        service.loop.run_forever()
    except KeyboardInterrupt:
        pass
