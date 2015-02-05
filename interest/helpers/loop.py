import asyncio


@property
def loop(self):
    return asyncio.get_event_loop()
