# ***** BEGIN LICENSE BLOCK *****
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. For a full copy of the MPL v2.0, see the LICENSE file accompanying
# this package.
#
# ***** END LICENSE BLOCK *****
__version__ = '0.9.14p0'

import logging
try:
    # not available in python 2.6
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Add NullHandler to prevent logging warnings
logging.getLogger(__name__).addHandler(NullHandler())

from pika.connection import ConnectionParameters
from pika.connection import URLParameters
from pika.credentials import PlainCredentials

from pika.adapters import AsyncoreConnection
from pika.adapters import BlockingConnection

# These require external dependencies

# LibEv - http://software.schmorp.de/pkg/libev.html
try:
    from pika.adapters import LibevConnection
except ImportError:
    pass

# Tornado - http://www.tornadoweb.org
try:
    from pika.adapters import TornadoConnection
except ImportError:
    pass

# Twisted - https://twistedmatrix.com/trac/
try:
    from pika.adapters import TwistedConnection
except ImportError:
    pass
