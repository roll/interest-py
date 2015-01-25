import asyncio
from functools import partial
from .binding import Binding


class http:

    # Public

    @classmethod
    def any(cls, param):
        return cls.__process(param)

    @classmethod
    def get(cls, param):
        return cls.__process(param, methods=['GET'])

    @classmethod
    def post(cls, param):
        return cls.__process(param, methods=['POST'])

    @classmethod
    def put(cls, param):
        return cls.__process(param, methods=['PUT'])

    @classmethod
    def delete(cls, param):
        return cls.__process(param, methods=['DELETE'])

    @classmethod
    def patch(cls, param):
        return cls.__process(param, methods=['PATCH'])

    @classmethod
    def head(cls, param):
        return cls.__process(param, methods=['HEAD'])

    @classmethod
    def options(cls, param):
        return cls.__process(param, methods=['OPTIONS'])

    # Private

    @classmethod
    def __process(cls, param, *, methods=None):
        if isinstance(param, str):
            return partial(cls.__register, path=param, methods=methods)
        return cls.__register(param, methods=methods)

    @classmethod
    def __register(cls, function, *, path=None, methods=None):
        factory = partial(Binding, path=path, methods=methods)
        if not asyncio.iscoroutine(function):
            function = asyncio.coroutine(function)
        setattr(function, Binding.MARKER, factory)
        return function