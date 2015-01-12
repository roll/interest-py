from .dispatcher import (Dispatcher, Resource,
                         Binding, get, post, put, delete, patch, head, options,
                         Match, ExistentMatch, NonExistentMatch)
from .formatter import Formatter, JSONFormatter
from .processor import Processor, Middleware
from .protocol import Protocol
from .service import Service
version = '0.0.0'  # REPLACE: version = '{{ version }}'
