# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""
Simple, Pythonic interface to RabbitMQ

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

from pika.amqp import connection
from pika.adapters import select_ioloop
from pika.authentication import plain
from pika.amqp import header

class RabbitMQ(object):

    def __init__(self, host='localhost', port=5672, vhost='/',
                 username='guest', password='password'):
        """
        Create a new RabbitMQ connection object

        :param str host: The hostname of the RabbitMQ broker to use
        :param int port: The port number of the RabbitMQ broker
        :param str vhost: The virtual host name to connect to
        :param str username: The username to connect as
        :param str password: The password to use

        """
        # Create the broker
        self._broker = connection.Broker(host, port, vhost)

        # Create our authentication object
        self._auth = plain.PlainAuth(username, password)

        # Create the IOLoop
        self._ioloop = select_ioloop.SelectIOLoop()

        # By default, we're only reading
        self._ioloop.set_events(self._broker.select_io,
                                self._ioloop.READ)

    def connect(self):
        """Connect to the RabbitMQ Broker
        """
        # Open the connection
        self._broker.open()

        # Send a new ProtocolHeader frame
        self._broker.send_frame(header.ProtocolHeader())
