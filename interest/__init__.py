from .dispatcher import (Binding, get, post, put, delete, patch, head, options,
                         Match, ExistentMatch, NonExistentMatch,
                         Dispatcher, Resource)
from .formatter import Formatter, JSONFormatter
from .middleware import Middleware
from .processor import Processor
from .protocol import Protocol
from .service import Service
version = '0.0.0'  # REPLACE: version = '{{ version }}'
