import asyncio
from aiohttp import web
from functools import partial
from .helpers import STICKER


class http:
    """HTTP library/proxy backed by aiohttp.web.

    .. seealso:: http://aiohttp.readthedocs.org/en/
    """

    # Public

    Request = web.Request
    StreamResponse = web.StreamResponse
    Response = web.Response
    WebSocketResponse = web.WebSocketResponse
    Exception = web.HTTPException
    Error = web.HTTPError
    Redirection = web.HTTPRedirection
    Successful = web.HTTPSuccessful
    Ok = web.HTTPOk
    Created = web.HTTPCreated
    Accepted = web.HTTPAccepted
    NonAuthoritativeInformation = web.HTTPNonAuthoritativeInformation
    NoContent = web.HTTPNoContent
    ResetContent = web.HTTPResetContent
    PartialContent = web.HTTPPartialContent
    MultipleChoices = web.HTTPMultipleChoices
    MovedPermanently = web.HTTPMovedPermanently
    Found = web.HTTPFound
    SeeOther = web.HTTPSeeOther
    NotModified = web.HTTPNotModified
    UseProxy = web.HTTPUseProxy
    TemporaryRedirect = web.HTTPTemporaryRedirect
    ClientError = web.HTTPClientError
    BadRequest = web.HTTPBadRequest
    Unauthorized = web.HTTPUnauthorized
    PaymentRequired = web.HTTPPaymentRequired
    Forbidden = web.HTTPForbidden
    NotFound = web.HTTPNotFound
    MethodNotAllowed = web.HTTPMethodNotAllowed
    NotAcceptable = web.HTTPNotAcceptable
    ProxyAuthenticationRequired = web.HTTPProxyAuthenticationRequired
    RequestTimeout = web.HTTPRequestTimeout
    Conflict = web.HTTPConflict
    Gone = web.HTTPGone
    LengthRequired = web.HTTPLengthRequired
    PreconditionFailed = web.HTTPPreconditionFailed
    RequestEntityTooLarge = web.HTTPRequestEntityTooLarge
    RequestURITooLong = web.HTTPRequestURITooLong
    UnsupportedMediaType = web.HTTPUnsupportedMediaType
    RequestRangeNotSatisfiable = web.HTTPRequestRangeNotSatisfiable
    ExpectationFailed = web.HTTPExpectationFailed
    ServerError = web.HTTPServerError
    InternalServerError = web.HTTPInternalServerError
    NotImplemented = web.HTTPNotImplemented
    BadGateway = web.HTTPBadGateway
    ServiceUnavailable = web.HTTPServiceUnavailable
    GatewayTimeout = web.HTTPGatewayTimeout
    VersionNotSupported = web.HTTPVersionNotSupported

    @classmethod
    def bind(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP endpoint.
        """
        def stick(function, **binding):
            if not asyncio.iscoroutine(function):
                function = asyncio.coroutine(function)
            bindings = getattr(function, STICKER, [])
            bindings.append(binding)
            setattr(function, STICKER, bindings)
            return function
        if isinstance(param, str):
            return partial(stick, prefix=param, **kwargs)
        return stick(param, **kwargs)

    @classmethod
    def get(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP get endpoint.
        """
        return cls.bind(param, methods=['GET'], **kwargs)

    @classmethod
    def post(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP post endpoint.
        """
        return cls.bind(param, methods=['POST'], **kwargs)

    @classmethod
    def put(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP put endpoint.
        """
        return cls.bind(param, methods=['PUT'], **kwargs)

    @classmethod
    def delete(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP delete endpoint.
        """
        return cls.bind(param, methods=['DELETE'], **kwargs)

    @classmethod
    def patch(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP patch endpoint.
        """
        return cls.bind(param, methods=['PATCH'], **kwargs)

    @classmethod
    def head(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP head endpoint.
        """
        return cls.bind(param, methods=['HEAD'], **kwargs)

    @classmethod
    def options(cls, param=None, **kwargs):
        """Bind middleware's method as HTTP options endpoint.
        """
        return cls.bind(param, methods=['OPTIONS'], **kwargs)
