"""
An AMQP Connection Encapsulation Object

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import logging

from pika import authentication
from pika.amqp import header
from pika.amqp import specification


class Connection(object):
    """Manages the AMQP connection state for the given adapter."""

    BASE_CHANNEL = 0

    def __init__(self, adapter):
        """Create the connection object passing in the adapter for reading
        and writing raw data.

        :param pika.adapters.base.Adapter adapter: The adapter

        """
        self._logger = logging.getLogger(__name__)
        self._adapter = adapter

        # By default we have no authenticating object
        self._authenticator = None

        # Not connected by default
        self._connected = False

    @property
    def connected(self):
        """Return the connection state.

        :return: bool

        """
        return self._connected

    def open(self, username=None, password=None):
        """Open the connection to the broker, using the specified username
        and password if no authenticator was previously set.

        :param str username: The username to connect as if using PlainAuth
        :param str password: The password to use if using PlainAuth.

        """
        if not self._authenticator:
            self._authenticator = authentication.PlainAuth(username, password)

        # Tell the Adapter Object to connect
        if self._adapter.connect():
            self._send_protocol_header()

    def send_frame(self, amqp_frame):
        """Send the frame to the IO object.

        :param amqp.frame.Frame amqp_frame: The frame to send.

        """
        self._logger.debug('Writing frame: %r', amqp_frame)

        # Send the frame to the IO object
        self._adapter.send(amqp_frame.marshal())


    def _send_protocol_header(self):
        """Send the protocol header to the remote server."""
        self.send_frame(header.ProtocolHeader())
        self._adapter.add_callback(self.BASE_CHANNEL,
                                   specification.Connection.Start,
                                   self.on_protocol_header)

    def on_protocol_header(self, channel, response):
        self._logger.debug('Received %r', response)
