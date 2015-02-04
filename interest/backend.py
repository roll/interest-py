import asyncio
from aiohttp import web
from functools import partial
from .helpers import STICKER


class http:
    """HTTP proxy library for aiohttp.

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
    def bind(cls, param):
        return cls.__register(param)

    @classmethod
    def get(cls, param):
        """Bind a get responder.
        """
        return cls.__register(param, methods=['GET'])

    @classmethod
    def post(cls, param):
        """Bind a post responder.
        """
        return cls.__register(param, methods=['POST'])

    @classmethod
    def put(cls, param):
        """Bind a put responder.
        """
        return cls.__register(param, methods=['PUT'])

    @classmethod
    def delete(cls, param):
        """Bind a delete responder.
        """
        return cls.__register(param, methods=['DELETE'])

    @classmethod
    def patch(cls, param):
        """Bind a patch responder.
        """
        return cls.__register(param, methods=['PATCH'])

    @classmethod
    def head(cls, param):
        """Bind a head responder.
        """
        return cls.__register(param, methods=['HEAD'])

    @classmethod
    def options(cls, param):
        """Bind a options responder.
        """
        return cls.__register(param, methods=['OPTIONS'])

    # Private

    @classmethod
    def __register(cls, param, *, methods=None):
        def stick(function, **params):
            if not asyncio.iscoroutine(function):
                function = asyncio.coroutine(function)
            setattr(function, STICKER, params)
            return function
        if isinstance(param, str):
            return partial(stick, path=param, methods=methods)
        return stick(param, methods=methods)
