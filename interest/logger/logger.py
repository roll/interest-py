import logging
from ..helpers import Config


class Logger(Config):
    """Base Logger class (abstract).

    Logger is used by :class:`.Service` for all logging purposes.
    Logger subclasses can use python's system logging module

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    system: object
        System logger.
    template: str
        Template for access formatting.

    Example
    -------
    For production use let's print the access log to the stdout
    and skip the debug log at all::

        class ProductionLogger(Logger):

            # Public

            SYSTEM = logging.getLogger('myapp')
            TEMPLATE = '%(host)s %(time)s and so on'

            def access(self, record):
                print(self.template % record)

            def debug(self, message, *args, **kwargs):
                pass

        service = Service(path='/api/v1', logger=ProductionLogger)

    .. seealso:: API: :class:`.Config`
    """

    # Public

    SYSTEM = logging.getLogger('interest')
    """System logget (default).
    """
    TEMPLATE = ('%(host)s %(time)s "%(request)s" %(status)s '
                '%(length)s "%(referer)s" "%(agent)s"')
    """Template for access formatting (default).
    """

    def __init__(self, service, *, system=None, template=None):
        if system is None:
            system = self.SYSTEM
        if template is None:
            template = self.TEMPLATE
        self.__service = service
        self.__system = system
        self.__template = template

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def system(self):
        """System logger (read-only).
        """
        return self.__system

    @property
    def template(self):
        """Template for access formatting (read-only).
        """
        return self.__template

    def access(self, record):
        """Log access event.

        Parameters
        ----------
        record: :class:`.Record`
            Record dict to use with template.
        """
        self.info(self.template % record)

    def debug(self, message, *args, **kwargs):
        """Log debug event.

        Compatible with logging.debug signature.
        """
        self.system.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Log info event.

        Compatible with logging.info signature.
        """
        self.system.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Log warning event.

        Compatible with logging.warning signature.
        """
        self.system.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """Log error event.

        Compatible with logging.error signature.
        """
        self.system.error(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        """Log exception event.

        Compatible with logging.exception signature.
        """
        self.system.exception(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """Log critical event.

        Compatible with logging.critical signature.
        """
        self.system.critical(message, *args, **kwargs)
