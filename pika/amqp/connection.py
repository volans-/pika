# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""
An AMQP Connection Encapsulation Object

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import logging
import socket
import StringIO

from pika.amqp import io

class Connection(object):
    """The connection object is not intended for end-developer usage but rather
    as a common Connection state management object to be used by Pika itself.

    """
    def __init__(self, broker):

        self._broker = broker


class Broker(object):
    """The broker object defines the attributes about the broker pika is to
    communicate with.

    """
    def __init__(self, host='localhost', port=5672, vhost='/'):
        """Create a new instance of a broker that can be used for connections
        to RabbitMQ.

        :param str host: The broker hostname or IP address
        :param int port: The broker port to connect on, default: 5672
        :param str vhost: The virtual-host on the broker to connect to

        """
        self._logger = logging.getLogger('pika.amqp.connection')

        # Specify our default parameters
        self._host = host
        self._port = port
        self._vhost = vhost

        # Create a socket
        # Create our socket and set our socket options
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

        # Create a new IO handler
        self._io = io.SocketIO(self._socket)

        # Create an output buffer
        self._buffer = StringIO.StringIO()

        # Send our open frame, then start the IOLoop

    def open(self):
        """Open the connection to the broker

        """
        self._socket.connect((self._host, self._port))

    @property
    def select_io(self):
        """Return the io.SelectIO object

        :returns io.select_io:

        """
        return self._io

    def send_frame(self, amqp_frame):

        self._logger.debug('Writing frame: %r', amqp_frame)
        # Append the frame to our buffer
        self._buffer.write(amqp_frame.marshal())


class SSLBroker(Broker):
    """The SSL broker extends the Broker object adding the various additional
    configuration knobs that a Broker needs to connect via SSL.

    """
    def __init__(self, host='localhost', port=5672, vhost='/'):
        Broker.__init__(self, host, port, vhost)
