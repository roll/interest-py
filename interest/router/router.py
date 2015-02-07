from urllib.parse import urlencode
from ..helpers import Config, Match
from .parser import StringParser, PathParser, IntegerParser, FloatParser
from .pattern import Pattern


class Router(Config):
    """Router is a component responsible for the routing.

    Router's only two fings to do are to check if request/constraints
    pair have :class:`.Match` or not and to costruct url back from
    the middleware name and the given parameters. Router uses
    :class:`.Parser` dict to handle placeholders in paths.
    Builtin parsers are liste below.

    .. seealso:: Implements:
        :class:`.Config`

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    parsers: dict
        Dictionary of the :class:`.Parser` sublasses.

    Builtin parsers
    ---------------
    - str
    - path
    - int
    - float

    Examples
    --------
    Let's see how match and url work::

        router = Router()
        match = router.match('<request>', '/some/path/<name:int>')
        url = router.url('name', **match)
    """

    # Public

    PARSERS = {}
    """Default parsers parameter.
    """


    def __init__(self, service, *, parsers=None):
        if parsers is None:
            parsers = self.PARSERS.copy()
        self.__service = service
        self.__add_parsers(parsers)
        self.__patterns = {}

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def match(self, request, *, root=None, path=None, methods=None):
        """Return match or None for the request/constraints pair.

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
        :class:`.Match`/None
            Match instance (True) or None (False).
        """
        match = Match()
        if path is not None:
            pattern = self.__get_pattern(path)
            match = pattern.match(request.path)
        elif root is not None:
            pattern = self.__get_pattern(root)
            match = pattern.match(request.path, left=True)
        if not match:
            return None
        if methods:
            methods = map(str.upper, methods)
            if request.method not in methods:
                return None
        return match

    def url(self, name, *, base=None, query=None, **match):
        """Construct an url for the given parameters.

        Parameters
        ----------
        name: str
            Nested middleware's name separated by dots.
        base: :class:`.Middleware`
            Base middleware to start searching from.
        query: dict
            Query string data.
        match: dict
            Path parameters.

        Returns
        -------
        str
            Constructed url.
        """
        if base is None:
            base = self.service
        for name in name.split('.'):
            base = base[name]
        pattern = self.__get_pattern(base.path)
        url = pattern.format(**match)
        if query is not None:
            url += '?' + urlencode(query)
        return url

    # Private

    __PARSERS = {
       'str': StringParser,
       'path': PathParser,
       'int': IntegerParser,
       'float': FloatParser}

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
