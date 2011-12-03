# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""
Manage IO on the socket connection

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import logging
import socket

from pika.amqp.specification import AMQP_FRAME_MAX_SIZE


class SocketIO(object):

    def __init__(self, socket_handle, frame_size=None):
        """Create a new SocketIO object.

        :param socket.socket socket_handle: The socket to read and write from
        :param int frame_size: The length to read from the socket

        """
        self._socket = socket_handle
        self._logger = logging.getLogger('pika.amqp.io')

        # Set the default frame size if we need it
        if not frame_size:
            self._buffer_size = frame_size or AMQP_FRAME_MAX_SIZE

    @property
    def file_descriptor(self):
        """Return the socket file descriptor

        :returns int: Socket file descriptor

        """
        return self._socket.fileno

    def read(self):
        """Read from the socket

        :returns: str or None
        :raises socket.error: Error raised on read

        """
        self._logger.debug('Reading up to %i bytes from %r',
                           self._buffer_size, self._socket)
        try:
            return self._socket.recv(self._buffer_size)
        except socket.error as error:
            self._logger.error('Socket error: %r', error)
            return None

    def write(self, data):
        """Write to teh socket

        :param str data: The data to write to the socket

        """
        self._logger.debug('Writing %i bytes to %r', len(data), self._socket)
        self._socket.send(data)
