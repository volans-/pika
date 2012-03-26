"""
broker.py

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-03-25'


import logging
from pika.amqp import connection
from pika.amqp import io
from pika.amqp import specification
from pika.adapters import blocking


class Broker(object):
    """The broker object defines the attributes about the broker pika is to
    communicate with.

    """
    def __init__(self, host=None, port=None, vhost=None, adapter=None):
        """Create a new instance of a broker that can be used for connections
        to RabbitMQ.

        :param str host: The broker hostname or IP address. If omitted, use
                         pika.amqp.specification.DEFAULT_HOST
        :param int port: The broker port to connect on
        :param str vhost: The virtual-host on the broker to connect to

        """
        self._logger = logging.getLogger(__name__)

        # Specify our default parameters
        self._vhost = vhost or specification.DEFAULT_VHOST

        # Create our socket IO object
        self._io = self._socket_io(host or specification.DEFAULT_HOST,
                                   port or specification.DEFAULT_PORT)

        # Setup the communication path adapter
        self._adapter = self._setup_adapter(adapter)

        # Create the protocol connection object
        self._connection = connection.Connection(self._adapter)

    def open(self, username=None, password=None):
        """Open the connection to the broker, using the specified username
        and password if no authenticator was previously set.

        :param str username: The username to connect as if using PlainAuth
        :param str password: The password to use if using PlainAuth.

        """
        self._connection.open(username, password)

    def _default_adapter(self):
        """Return an instance of the default adapter object.

        """
        return blocking.Adapter()

    def _setup_adapter(self, adapter):
        """Assign the adapter or the default adapter to the object.

        :param pika.adapters.base.Adapter adapter: The adapter object

        """
        adapter = adapter or self._default_adapter()
        adapter.set_io(self._io)
        return adapter

    def _socket_io(self, host, port):
        """Return the SocketIO object for the broker connection.

        """
        return io.SocketIO(host, port)



class SSLBroker(Broker):
    """The SSL broker extends the Broker object adding the various additional
    configuration knobs that a Broker needs to connect via SSL.

    """
    def __init__(self, host='localhost', port=5672, vhost='/'):
        super(SSLBroker, self).__init__(host, port, vhost)
