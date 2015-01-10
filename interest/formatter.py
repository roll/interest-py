import json
from abc import ABCMeta, abstractmethod
from aiohttp.web import Response


class Formatter(metaclass=ABCMeta):

    # Public

    def make_response(self, data):
        text = self.encode(data)
        response = Response(text=text, content_type=self.content_type)
        return response

    @property
    @abstractmethod
    def content_type(self):
        pass  # pragma: no cover

    @abstractmethod
    def decode(self, text):
        pass  # pragma: no cover

    @abstractmethod
    def encode(self, data):
        pass  # pragma: no cover


class JSONFormatter(Formatter):

    # Public

    content_type = 'application/json'

    def decode(self, text):
        return json.loads(text)

    def encode(self, data):
        return json.dumps(data)
