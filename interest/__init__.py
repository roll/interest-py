from .binding import Binding, get, post, put, delete, patch, head, options
from .dispatcher import Dispatcher
from .formatter import Formatter, JSONFormatter
from .match import Match, ExistentMatch, NonExistentMatch
from .middleware import Middleware
from .processor import Processor
from .protocol import Protocol
from .resource import Resource
from .service import Service
version = '0.0.0'  # REPLACE: version = '{{ version }}'
