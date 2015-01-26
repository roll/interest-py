Tips & Tricks
=============

How to start a server manually?
-------------------------------

Just use handler.fork as a protocol factory for asyncio. You can start as many 
servers on different ports as you want:

.. code-block:: python

    import asyncio
    from interest import Service
    
    service = Service(path='/api/v1')
    loop = ayncio.get_event_loop()
    server = loop.create_server(self.service.handler.fork, '127.0.0.1', 9000)
    server = loop.run_until_complete(server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
