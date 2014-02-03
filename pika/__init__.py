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

from pika.connection import ConnectionParameters
from pika.connection import URLParameters
from pika.credentials import PlainCredentials
from pika.spec import BasicProperties

from pika.adapters import BaseConnection
from pika.adapters import AsyncoreConnection
from pika.adapters import BlockingConnection
from pika.adapters import SelectConnection
from pika.adapters import TornadoConnection
from pika.adapters import TwistedConnection
from pika.adapters import LibevConnection

# Add NullHandler to prevent logging warnings
logging.getLogger(__name__).addHandler(NullHandler())
