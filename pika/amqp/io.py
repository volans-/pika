"""
Manage IO on the socket connection

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import collections
import logging
import socket

from pika.amqp import frame
from pika.amqp import specification


class SocketIO(object):

    def __init__(self, host, port, frame_size=None):
        """Create a new SocketIO object.

        :param str host: The ip address or hostname to connect to
        :param int port: The TCP port to connect on
        :param int frame_size: The length to read from the socket

        """
        self._logger = logging.getLogger(__name__)

        # Set the default frame size if we need it
        self._buffer_size = frame_size or specification.FRAME_MAX_SIZE

        # Store the connection parameters
        self._connect_params = (host, port)

        # Create the socket
        self._socket = self._create_socket()

        # Create our input and output buffers
        self._input_buffer = collections.deque()
        self._output_buffer = collections.deque()

    def close(self):
        """Close the socket"""
        self._socket.close()
        self._logger.debug('Socket closed')

    def connect(self):
        """Connect to the remote socket specified in the constructor."""
        self._logger.debug('Connecting to %r', self._connect_params)
        try:
            self._socket.connect(self._connect_params)
        except socket.error as error:
            self._logger.error('Error connecting to %r: %s',
                               self._connect_params, error)
            self._socket.close()
            return False

        # Return that the socket connected
        return True

    def _create_socket(self):
        """Create a new socket, set the options on it and return the socket
        handle.

        :return socket.socket: The new socket to act on

        """
        handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        handle.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        self._logger.debug('Socket created: %r', handle)
        return handle

    def read(self):
        """When called, append data to the right side of the input stack.

        This object should be called by the adapter object when the socket
        is ready to be read from.

        """
        if len(self._input_buffer):
            return self._input_buffer.popleft()

    def recv(self):
        """Read from the socket

        :raises socket.error: Error raised on read

        """
        self._logger.debug('Reading up to %i bytes from %r',
                           self._buffer_size,
                           self._socket)
        try:
            data = self._socket.recv(self._buffer_size)
        except socket.error as error:
            self._logger.error('Socket error: %r', error)
            return

        if data:
            self._logger.debug('Appending %i bytes to the buffer', len(data))
            self._input_buffer.append(data)

    def sendall(self):
        """Write a single item off the left side of the stack to the socket.

        This method should be called by the adapter object when the socket
        is ready to write.

        """
        data = self._output_buffer.popleft()
        self._logger.debug('Writing %r to %r', data, self._socket)
        try:
            self._socket.sendall(data)
        except socket.error as error:
            self._logger.error('Error sending to socket: %r', error)
            self._socket.close()
            return False
        return True

    def write(self, data):
        """Append data to the deque object to be sent.

        :param str data: The data to send

        """
        self._output_buffer.append(data)
