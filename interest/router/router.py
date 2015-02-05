from ..helpers import Config, ExistentMatch, NonExistentMatch
from .parser import Parser
from .pattern import Pattern


class Router(Config):
    """Router implementation.

    .. seealso:: API: :class:`.Config`
    """

    # Public

    PARSERS = {}

    def __init__(self, service, *, parsers=None):
        if parsers is None:
            parsers = self.PARSERS
        self.__service = service
        self.__add_parsers(parsers)
        self.__patterns = {}

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    def match(self, request, *, root=None, path=None, methods=None):
        """Check if request matchs the given parameters.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        root: str
            HTTP path root.
        path: str
            HTTP path.
        methods: list
            HTTP methods.

        Returns
        -------
        :class:`.Match`
            Match instance.
        """
        match = ExistentMatch()
        if path is not None:
            pattern = self.__get_pattern(path)
            match = pattern.match(request.path)
        elif root is not None:
            pattern = self.__get_pattern(root)
            match = pattern.match(request.path, left=True)
        if not match:
            return NonExistentMatch()
        if methods:
            methods = map(str.upper, methods)
            if request.method not in methods:
                return NonExistentMatch()
        return match

    # Private

    __PARSERS = {
       'str': Parser.config(pattern=r'[^<>/]+'),
       'path': Parser.config(pattern=r'[^<>]+'),
       'int': Parser.config(pattern=r'[1-9]+', convert=int),
       'float': Parser.config(pattern=r'[1-9.]+', convert=float)}

    def __add_parsers(self, parsers):
        self.__parsers = {}
        eparsers = self.__PARSERS.copy()
        eparsers.update(parsers)
        for key, cls in eparsers.items():
            self.__parsers[key] = cls(self)

    def __get_pattern(self, path):
        if path not in self.__patterns:
            self.__patterns[path] = Pattern.create(
                path, self.__parsers)
        return self.__patterns[path]
