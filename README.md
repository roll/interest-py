# Interest

[![Travis](https://img.shields.io/travis/inventive-ninja/interest.svg)](https://travis-ci.org/inventive-ninja/interest)
[![Coveralls](https://img.shields.io/coveralls/inventive-ninja/interest.svg?branch=master)](https://coveralls.io/r/inventive-ninja/interest?branch=master)
[![PyPI](https://img.shields.io/pypi/v/interest.svg)](https://pypi.org/project/interest)

Event-driven web framework on top of aiohttp/asyncio.

## Features

- event-driven on top of aiohttp/asyncio
- consistent, modular and flexible flow model, class-based
- configurable and pluggable

## Example

Install interest package:

```
$ pip install interest
```

Save the following code as `server.py`:


```python
# server.py
from interest import Service, http

class Service(Service):

    # Public

    @http.get('/')
    def hello(self, request):
        return http.Response(text='Hello World!')


# Listen forever
service = Service()
service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
```

Run the server in the terminal and use another to interact:

```
$ python server.py
...
$ curl -X GET http://127.0.0.1:9000/; echo
Hello World!
...
```

## Read more

Please visit Interest's developer hub to get docs, news and support:

[Developer Hub](https://interest.readme.io/)

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
