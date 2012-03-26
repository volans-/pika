"""
blocking.py

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-03-25'

from pika.adapters import base


class Adapter(base.Adapter):

    def __init__(self):
        super(Adapter, self).__init__()


    def add_callback(self, channel, expectation, callback):
        """Add the method specified to the callback data structure for the
        given channel and frame type.

        :param int channel: Channel number
        :param any expectation: The frame obj or class to add the callback for
        :param function callback: The method to add the callback for

        """
        # In the case where we expect a response, do blocking reads
        while True:
            channel, response = self.read()
            if isinstance(response, expectation):
                callback(channel, response)
                break

    def send(self, value):
        """Blocking adapter doesn't wait until write is ready, it just does a
        blocking write.

        :param str value: The value to write out

        """
        self._io.write(value)
        self._io.sendall()

    def read(self):
        """Blocking adapter doesn't wait until read is ready, it just does a
        blocking read.

        :return: str

        """
        self._io.recv()
        return self.demarshal(self._io.read())
