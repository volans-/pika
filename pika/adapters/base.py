"""
base.py

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-03-25'

import logging

from pika import callback_manager
from pika.amqp import frame



class Adapter(object):
    """Base adapter object"""

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._io = None
        # Create a callback manager object
        self._callbacks = self._callback_manager()

    def add_callback(self, channel, frame, callback):
        """Add the method specified to the callback data structure for the
        given channel and frame type.

        :param int channel: Channel number
        :param any frame: The frame obj or class to add the callback for
        :param function callback: The method to add the callback for

        """
        self._callbacks.add(channel, frame, callback)

    def connect(self):
        return self._io.connect()

    def on_read_ready(self):
        return self._io.read()

    def on_send_ready(self):
        self._io.sendall()

    def demarshal(self, data):

        bytes, channel, value = frame.demarshal(data)

        return channel, value



    def read(self):
        raise NotImplementedError

    def send(self, value):
        self._io.write(value)

    def set_io(self, io):
        self._io = io

    def _callback_manager(self):
        """Return an callback manager object.

        :return: pika.callback_manager.CallbackManager

        """
        return callback_manager.CallbackManager()
