from abc import ABCMeta
from ..helpers import Configurable


class Logger(Configurable, metaclass=ABCMeta):
    """Base Logger class (abstract).

    Logger is used by :class:`.Service` for all logging purposes.
    Logger subclasses can use python's system logging module
    (see :class:`.SystemLogger`) or something other. But main
    concept about Logger is to be proxy layer between application/interest
    logging needs and concrete logging systems/implementations.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Example
    -------
    Logger is abstract just formally. We can implenent a no-op
    logger doing nothing::

        class NoopLogger(Logger):

            # Public

            pass

        service = Service(path='/api/v1', logger=NoopLogger)
    """

    # Public

    TEMPLATE = ('%(host)s %(time)s "%(request)s" %(status)s '
                '%(length)s "%(referer)s" "%(agent)s"')
    """Template for access formatting (default).
    """

    def __init__(self, service, *, template=None):
        if template is None:
            template = self.TEMPLATE
        self.__service = service
        self.__template = template

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def template(self):
        """Template for access formatting (read-only).
        """
        return self.__template

    def access(self, record):
        """Log access event (no-op).

        Parameters
        ----------
        record: :class:`.Record`
            Record dict to use with template.
        """
        pass

    def debug(self, message, *args, **kwargs):
        """Log debug event (no-op).

        Compatible with logging.debug signature.
        """
        pass

    def info(self, message, *args, **kwargs):
        """Log info event (no-op).

        Compatible with logging.info signature.
        """
        pass

    def warning(self, message, *args, **kwargs):
        """Log warning event (no-op).

        Compatible with logging.warning signature.
        """
        pass

    def error(self, message, *args, **kwargs):
        """Log error event (no-op).

        Compatible with logging.error signature.
        """
        pass

    def exception(self, message, *args, **kwargs):
        """Log exception event (no-op).

        Compatible with logging.exception signature.
        """
        pass

    def critical(self, message, *args, **kwargs):
        """Log critical event (no-op).

        Compatible with logging.critical signature.
        """
        pass
