# flake8: noqa
import logging

from .about import __version__
from .candidate import Candidate
from .ice import Connection, ConnectionClosed, TransportPolicy

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
