from aiohttp.helpers import atoms


class Interaction(dict):
    """Interaction representation.
    """

    # Public

    def __init__(self, *, request, response, transport, duration):
        self.__request = request
        self.__response = response
        self.__transport = transport
        self.__duration = duration
        self.__extended = False
        self.__populate()

    def __missing__(self, key):
        if self.extended:
            headers = None
            if key.startswith('{'):
                if key.endswith('}i'):
                    headers = self.__request
                elif key.endswith('}o'):
                    headers = self.__response
            if headers is not None:
                return headers.get(key[1:-2], '-')
        return '-'

    @property
    def extended(self):
        return self.__extended

    @extended.setter
    def extended(self, value):
        self.__extended = value

    # Private

    def __populate(self):
        data = atoms(
            self.__request, None, self.__response,
            self.__transport, self.__duration)
        self['agent'] = data.get('a', '-')
        self['duration'] = data.get('D', '-')
        self['host'] = data.get('h', '-')
        self['lenght'] = data.get('l', '-')
        self['process'] = data.get('p', '-')
        self['referer'] = data.get('r', '-')
        self['request'] = data.get('r', '-')
        self['status'] = data.get('s', '-')
        self['time'] = data.get('t', '-')
