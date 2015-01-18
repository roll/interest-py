import json
from .formatter import Formatter


class JSONFormatter(Formatter):
    """JSONFormatter representation.
    """

    # Public

    content_type = 'application/json'

    def decode(self, text):
        return json.loads(text)

    def encode(self, data):
        return json.dumps(data)
