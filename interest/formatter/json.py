import json
from .formatter import Formatter


class JSONFormatter(Formatter):
    """Formatter implementation for JSON.

    Example
    -------
    For example we want to sign all data::

        class SignedJSONFormatter(JSONFormatter):

            # Public

            def encode(self, data):
                data['sign'] = True
                return super().encode(data)

        service = Service(path='/api/v1', formatter=SignedJSONFormatter)

    Make some encode/decode and check content_type::

        >>> service.formatter.encode({'hello': 'world'})
        '{"hello": "world", "sign": true}'
        >>> service.formatter.decode('{"value": true}')
        {'value': True}
        >>> service.formatter.content_type
        'application/json'

    .. seealso:: API: :class:`.Formatter`
    """

    # Public

    content_type = 'application/json'

    def decode(self, text):
        return json.loads(text)

    def encode(self, data):
        return json.dumps(data)
