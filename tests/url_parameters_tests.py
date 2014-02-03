from pamqp import specification
import ssl
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pika.connection import credentials
from pika.connection import parameters

class DefaultAMQPTests(unittest.TestCase):

    URL = 'amqp://localhost'

    def setUp(self):
        self.parameters = parameters.URLParameters(self.URL)

    def test_scheme(self):
        self.assertFalse(self.parameters.ssl)

    def test_host(self):
        self.assertEqual(self.parameters.host, 'localhost')

    def test_port(self):
        self.assertEqual(self.parameters.port, 5672)

    def test_virtual_host(self):
        self.assertEqual(self.parameters.virtual_host, '/')

    def test_username(self):
        self.assertEqual(self.parameters.username, 'guest')

    def test_password(self):
        self.assertEqual(self.parameters.password, 'guest')

    def test_credentials(self):
        self.assertIsInstance(self.parameters.credentials,
                              credentials.PlainCredentials)

    def test_credentials_username(self):
        self.assertEqual(self.parameters.credentials.username, 'guest')

    def test_credentials_password(self):
        self.assertEqual(self.parameters.credentials.password, 'guest')

    def test_heartbeat_interval(self):
        self.assertEqual(self.parameters.heartbeat_interval, 0)

    def test_connection_attempts(self):
        self.assertEqual(self.parameters.connection_attempts, 1)

    def test_channel_max(self):
        self.assertEqual(self.parameters.channel_max, 0)

    def test_frame_max(self):
        self.assertEqual(self.parameters.frame_max,
                         specification.FRAME_MAX_SIZE)

    def test_retry_delay(self):
        self.assertEqual(self.parameters.retry_delay, 2.0)

    def test_socket_timeout(self):
        self.assertEqual(self.parameters.socket_timeout, 0.25)


class AMQPOptionsTests(unittest.TestCase):

    URL = 'amqp://foo:bar@qux:5673/corgie?heartbeat_interval=120&' \
          'connection_attempts=5&channel_max=200&frame_max=32768&' \
          'locale=en_UK&retry_delay=3&socket_timeout=10'

    def setUp(self):
        self.parameters = parameters.URLParameters(self.URL)

    def test_scheme(self):
        self.assertFalse(self.parameters.ssl)

    def test_host(self):
        self.assertEqual(self.parameters.host, 'qux')

    def test_port(self):
        self.assertEqual(self.parameters.port, 5673)

    def test_virtual_host(self):
        self.assertEqual(self.parameters.virtual_host, 'corgie')

    def test_username(self):
        self.assertEqual(self.parameters.username, 'foo')

    def test_password(self):
        self.assertEqual(self.parameters.password, 'bar')

    def test_credentials(self):
        self.assertIsInstance(self.parameters.credentials,
                              credentials.PlainCredentials)

    def test_credentials_username(self):
        self.assertEqual(self.parameters.credentials.username, 'foo')

    def test_credentials_password(self):
        self.assertEqual(self.parameters.credentials.password, 'bar')

    def test_heartbeat_interval(self):
        self.assertEqual(self.parameters.heartbeat_interval, 120)

    def test_connection_attempts(self):
        self.assertEqual(self.parameters.connection_attempts, 5)

    def test_channel_max(self):
        self.assertEqual(self.parameters.channel_max, 200)

    def test_frame_max(self):
        self.assertEqual(self.parameters.frame_max, 32768)

    def test_retry_delay(self):
        self.assertEqual(self.parameters.retry_delay, 3)

    def test_socket_timeout(self):
        self.assertEqual(self.parameters.socket_timeout, 10)


class AMQPSOptionsTests(unittest.TestCase):

    URL = 'amqps://localhost/%2f?ssl=t&ssl_options=%7B%27ssl_version%27%3A+1%7D'

    def setUp(self):
        self.parameters = parameters.URLParameters(self.URL)

    def test_scheme(self):
        self.assertTrue(self.parameters.ssl)

    def test_port(self):
        self.assertEqual(self.parameters.port, 5671)

    def test_virtual_host(self):
        self.assertEqual(self.parameters.virtual_host, '/')

    def test_username(self):
        self.assertEqual(self.parameters.username, 'guest')

    def test_password(self):
        self.assertEqual(self.parameters.password, 'guest')

    def test_credentials(self):
        self.assertIsInstance(self.parameters.credentials,
                              credentials.PlainCredentials)

    def test_credentials_username(self):
        self.assertEqual(self.parameters.credentials.username, 'guest')

    def test_credentials_password(self):
        self.assertEqual(self.parameters.credentials.password, 'guest')

    def test_ssl_options_ssl_version(self):
        self.assertEqual(self.parameters.ssl_options['ssl_version'],
                         ssl.PROTOCOL_SSLv3)
