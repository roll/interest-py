import asyncio
from aiohttp import web
from functools import partial
from .helpers import STICKER


class http:
    """HTTP library/proxy backed by aiohttp.web.

    Part of the documetation is loaded from aiohttp package by Sphinx.

    .. note:: © Copyright 2013, 2014, 2015, KeepSafe.
    .. seealso::
        - `Documentation of aiohttp <http://aiohttp.readthedocs.org/en/>`_
        - `HTTP 1.1 specification <http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html>`_
        - `HTTP 1.1 update <http://evertpot.com/http-11-updated/>`_
    """

    # Public

    Request = web.Request
    """Request.
    """
    StreamResponse = web.StreamResponse
    """Stream response.
    """
    Response = web.Response
    """Response.
    """
    WebSocketResponse = web.WebSocketResponse
    """WebSocket response.
    """
    Exception = web.HTTPException
    """Exception.
    """
    Successful = web.HTTPSuccessful
    """2xx Successful.
    """
    Ok = web.HTTPOk
    """200 OK.
    """
    Created = web.HTTPCreated
    """201 Created.
    """
    Accepted = web.HTTPAccepted
    """202 Accepted.
    """
    NonAuthoritativeInformation = web.HTTPNonAuthoritativeInformation
    """203 Non-Authoritative Information.
    """
    NoContent = web.HTTPNoContent
    """204 No Content.
    """
    ResetContent = web.HTTPResetContent
    """205 Reset Content.
    """
    PartialContent = web.HTTPPartialContent
    """206 Partial Content.
    """
    Redirection = web.HTTPRedirection
    """3xx Redirection.
    """
    MultipleChoices = web.HTTPMultipleChoices
    """300 Multiple Choices.
    """
    MovedPermanently = web.HTTPMovedPermanently
    """301 Moved Permanently.
    """
    Found = web.HTTPFound
    """302 Found.
    """
    SeeOther = web.HTTPSeeOther
    """303 See Other.
    """
    NotModified = web.HTTPNotModified
    """304 Not Modified.
    """
    UseProxy = web.HTTPUseProxy
    """305 Use Proxy.
    """
    TemporaryRedirect = web.HTTPTemporaryRedirect
    """307 Temporary Redirect.
    """
    Error = web.HTTPError
    """4/5xx Client or Server Error.
    """
    ClientError = web.HTTPClientError
    """4xx Client Error.
    """
    BadRequest = web.HTTPBadRequest
    """400 Bad Request.
    """
    Unauthorized = web.HTTPUnauthorized
    """401 Unauthorized.
    """
    PaymentRequired = web.HTTPPaymentRequired
    """402 Payment Required.
    """
    Forbidden = web.HTTPForbidden
    """403 Forbidden.
    """
    NotFound = web.HTTPNotFound
    """404 Not Found.
    """
    MethodNotAllowed = web.HTTPMethodNotAllowed
    """405 Method Not Allowed.
    """
    NotAcceptable = web.HTTPNotAcceptable
    """406 Not Acceptable.
    """
    ProxyAuthenticationRequired = web.HTTPProxyAuthenticationRequired
    """407 Proxy Authentication Required.
    """
    RequestTimeout = web.HTTPRequestTimeout
    """408 Request Timeout.
    """
    Conflict = web.HTTPConflict
    """409 Conflict.
    """
    Gone = web.HTTPGone
    """410 Gone.
    """
    LengthRequired = web.HTTPLengthRequired
    """411 Length Required.
    """
    PreconditionFailed = web.HTTPPreconditionFailed
    """412 Precondition Failed.
    """
    RequestEntityTooLarge = web.HTTPRequestEntityTooLarge
    """413 Request Entity Too Large.
    """
    RequestURITooLong = web.HTTPRequestURITooLong
    """414 Request-URI Too Long.
    """
    UnsupportedMediaType = web.HTTPUnsupportedMediaType
    """415 Unsupported Media Type.
    """
    RequestRangeNotSatisfiable = web.HTTPRequestRangeNotSatisfiable
    """416 Requested Range Not Satisfiable.
    """
    ExpectationFailed = web.HTTPExpectationFailed
    """417 Expectation Failed.
    """
    ServerError = web.HTTPServerError
    """5xx Server Error.
    """
    InternalServerError = web.HTTPInternalServerError
    """500 Internal Server Error.
    """
    NotImplemented = web.HTTPNotImplemented
    """501 Not Implemented.
    """
    BadGateway = web.HTTPBadGateway
    """502 Bad Gateway.
    """
    ServiceUnavailable = web.HTTPServiceUnavailable
    """503 Service Unavailable.
    """
    GatewayTimeout = web.HTTPGatewayTimeout
    """504 Gateway Timeout.
    """
    VersionNotSupported = web.HTTPVersionNotSupported
    """505 HTTP Version Not Supported.
    """

    @classmethod
    def bind(cls, param=None, **kwargs):
        """Bind middleware's method as endpoint.
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
    def options(cls, param=None, **kwargs):
        """Bind middleware's method as OPTIONS endpoint.
        """
        return cls.bind(param, methods=['OPTIONS'], **kwargs)

    @classmethod
    def get(cls, param=None, **kwargs):
        """Bind middleware's method as GET endpoint.
        """
        return cls.bind(param, methods=['GET'], **kwargs)

    @classmethod
    def head(cls, param=None, **kwargs):
        """Bind middleware's method as HEAD endpoint.
        """
        return cls.bind(param, methods=['HEAD'], **kwargs)

    @classmethod
    def post(cls, param=None, **kwargs):
        """Bind middleware's method as POST endpoint.
        """
        return cls.bind(param, methods=['POST'], **kwargs)

    @classmethod
    def put(cls, param=None, **kwargs):
        """Bind middleware's method as PUT endpoint.
        """
        return cls.bind(param, methods=['PUT'], **kwargs)

    @classmethod
    def delete(cls, param=None, **kwargs):
        """Bind middleware's method as DELETE endpoint.
        """
        return cls.bind(param, methods=['DELETE'], **kwargs)

    @classmethod
    def patch(cls, param=None, **kwargs):
        """Bind middleware's method as PATCH endpoint.
        """
        return cls.bind(param, methods=['PATCH'], **kwargs)
