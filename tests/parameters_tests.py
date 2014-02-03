from pamqp import specification
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pika.connection import credentials
from pika.connection import parameters


class BaseDefaultTests(unittest.TestCase):

    def setUp(self):
        self.parameters = parameters.Base()

    def test_repr(self):
        self.assertEqual(repr(self.parameters),
                         '<Base host=localhost port=5672 virtual_host=/ '
                         'ssl=False>')

    def test_backpressure_detection(self):
        self.assertFalse(self.parameters.backpressure_detection)

    def test_connection_attempts(self):
        self.assertEqual(self.parameters.connection_attempts, 1)

    def test_channel_max(self):
        self.assertEqual(self.parameters.channel_max, 0)

    def test_frame_max(self):
        self.assertEqual(self.parameters.frame_max,
                         specification.FRAME_MAX_SIZE)
    def test_heartbeat_interval(self):
        self.assertEqual(self.parameters.heartbeat_interval, 0)

    def test_host(self):
        self.assertEqual(self.parameters.host, 'localhost')

    def test_locale(self):
        self.assertEqual(self.parameters.locale, 'en_US')

    def test_password(self):
        self.assertEqual(self.parameters.password, 'guest')

    def test_port(self):
        self.assertEqual(self.parameters.port, 5672)

    def test_retry_delay(self):
        self.assertEqual(self.parameters.retry_delay, 2.0)

    def test_socket_timeout(self):
        self.assertEqual(self.parameters.socket_timeout, 0.25)

    def test_ssl_enabled(self):
        self.assertFalse(self.parameters.ssl)

    def test_ssl_options(self):
        self.assertDictEqual(self.parameters.ssl_options, {})

    def test_username(self):
        self.assertEqual(self.parameters.username, 'guest')

    def test_virtual_host(self):
        self.assertEqual(self.parameters.virtual_host, '/')


class BaseValidationTests(unittest.TestCase):

    def test_backpressure_detection_true(self):
        self.assertTrue(parameters.Base.validate_backpressure(True))

    def test_backpressure_detection_false(self):
        self.assertTrue(parameters.Base.validate_backpressure(False))

    def test_backpressure_detection_invalid_int(self):
        self.assertRaises(TypeError, parameters.Base.validate_backpressure, 0)

    def test_backpressure_detection_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_backpressure,
                          None)

    def test_backpressure_detection_invalid_str(self):
        self.assertRaises(TypeError, parameters.Base.validate_backpressure, '0')

    def test_channel_max_int(self):
        self.assertTrue(parameters.Base.validate_channel_max(10))

    def test_channel_max_invalid_float(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_channel_max,
                          5.0)

    def test_channel_max_invalid_none(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_channel_max,
                          None)

    def test_channel_max_invalid_str(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_channel_max,
                          '10')

    def test_channel_max_too_low(self):
        self.assertRaises(ValueError,
                          parameters.Base.validate_channel_max,
                          -1)

    def test_channel_max_too_high(self):
        self.assertRaises(ValueError,
                          parameters.Base.validate_channel_max,
                          204800)

    def test_connection_attempts_int(self):
        self.assertTrue(parameters.Base.validate_connection_attempts(10))

    def test_connection_attempts_invalid_float(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_connection_attempts,
                          5.0)

    def test_connection_attempts_invalid_none(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_connection_attempts,
                          None)

    def test_connection_attempts_invalid_str(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_connection_attempts,
                          '10')

    def test_connection_attempts_too_low(self):
        self.assertRaises(ValueError,
                          parameters.Base.validate_connection_attempts,
                          -1)

    def test_credentials_external(self):
        value = credentials.ExternalCredentials()
        self.assertTrue(parameters.Base.validate_credentials(value))

    def test_credentials_plain(self):
        value = credentials.PlainCredentials('guest', 'guest')
        self.assertTrue(parameters.Base.validate_credentials(value))

    def test_credentials_invalid(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_credentials,
                          ('guest', 'guest'))

    def test_frame_max_int(self):
        self.assertTrue(parameters.Base.validate_frame_max(32768))

    def test_frame_max_invalid_float(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_frame_max,
                          5.0)

    def test_frame_max_invalid_none(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_frame_max,
                          None)

    def test_frame_max_invalid_str(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_frame_max,
                          '10')

    def test_frame_max_too_big(self):
        self.assertRaises(ValueError, parameters.Base.validate_frame_max,
                          204800)

    def test_frame_max_too_small(self):
        self.assertRaises(ValueError, parameters.Base.validate_frame_max, 1024)

    def test_heartbeat_interval_int(self):
        self.assertTrue(parameters.Base.validate_heartbeat_interval(10))

    def test_heartbeat_interval_invalid_float(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_heartbeat_interval,
                          5.0)

    def test_heartbeat_interval_invalid_none(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_heartbeat_interval,
                          None)

    def test_heartbeat_interval_invalid_str(self):
        self.assertRaises(TypeError,
                          parameters.Base.validate_heartbeat_interval,
                          '10')

    def test_heartbeat_interval_too_low(self):
        self.assertRaises(ValueError,
                          parameters.Base.validate_heartbeat_interval,
                          -1)

    def test_host_bytes(self):
        self.assertTrue(parameters.Base.validate_host(b'foo'))

    def test_host_str(self):
        self.assertTrue(parameters.Base.validate_host('foo'))

    @unittest.skipIf(sys.version_info[0] == 3, 'No unicode obj in 3')
    def test_host_unicode(self):
        self.assertTrue(parameters.Base.validate_host(unicode('foo')))

    def test_host_invalid_int(self):
        self.assertRaises(TypeError, parameters.Base.validate_host, 10)

    def test_host_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_host, None)

    def test_locale_bytes(self):
        self.assertTrue(parameters.Base.validate_locale(b'foo'))

    def test_locale_str(self):
        self.assertTrue(parameters.Base.validate_locale('foo'))

    @unittest.skipIf(sys.version_info[0] == 3, 'No unicode obj in 3')
    def test_locale_unicode(self):
        self.assertTrue(parameters.Base.validate_locale(unicode('foo')))

    def test_locale_invalid_int(self):
        self.assertRaises(TypeError, parameters.Base.validate_locale, 10)

    def test_locale_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_locale, None)

    def test_port_int(self):
        self.assertTrue(parameters.Base.validate_port(10))

    def test_port_invalid_float(self):
        self.assertRaises(TypeError, parameters.Base.validate_port, 5.0)

    def test_port_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_port, None)

    def test_port_invalid_str(self):
        self.assertRaises(TypeError, parameters.Base.validate_port, '10')

    def test_retry_delay_int(self):
        self.assertTrue(parameters.Base.validate_retry_delay(10))

    def test_retry_delay_float(self):
        self.assertTrue(parameters.Base.validate_retry_delay(5.0))

    def test_retry_delay_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_retry_delay, None)

    def test_retry_delay_invalid_str(self):
        self.assertRaises(TypeError, parameters.Base.validate_retry_delay, '10')

    def test_retry_delay_too_low(self):
        self.assertRaises(ValueError,
                          parameters.Base.validate_retry_delay,
                          -1)

    def test_socket_timeout_int(self):
        self.assertTrue(parameters.Base.validate_socket_timeout(10))

    def test_socket_timeout_float(self):
        self.assertTrue(parameters.Base.validate_socket_timeout(5.0))

    def test_socket_timeout_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_socket_timeout,
                          None)

    def test_socket_timeout_invalid_str(self):
        self.assertRaises(TypeError, parameters.Base.validate_socket_timeout,
                          '10')

    def test_socket_timeout_too_low(self):
        self.assertRaises(ValueError,
                          parameters.Base.validate_socket_timeout,
                          -1)

    def test_ssl_true(self):
        self.assertTrue(parameters.Base.validate_ssl(True))

    def test_ssl_false(self):
        self.assertTrue(parameters.Base.validate_ssl(False))

    def test_ssl_invalid_int(self):
        self.assertRaises(TypeError, parameters.Base.validate_ssl, 0)

    def test_ssl_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_ssl, None)

    def test_ssl_invalid_str(self):
        self.assertRaises(TypeError, parameters.Base.validate_ssl, '0')

    def test_ssl_options_dict(self):
        self.assertTrue(parameters.Base.validate_ssl_options(dict()))

    def test_ssl_options_none(self):
        self.assertTrue(parameters.Base.validate_ssl_options(None))

    def test_ssl_options_valid_option(self):
        value = {'ciphers': 'ALL:SSLv2'}
        self.assertTrue(parameters.Base.validate_ssl_options(value))

    def test_ssl_options_valid_ssl_version(self):
        value = {'ssl_version': 2}
        self.assertTrue(parameters.Base.validate_ssl_options(value))

    def test_ssl_options_invalid_int(self):
        self.assertRaises(TypeError, parameters.Base.validate_ssl_options, 0)

    def test_ssl_options_invalid_str(self):
        self.assertRaises(TypeError, parameters.Base.validate_ssl_options, '0')

    def test_ssl_options_invalid_option(self):
        self.assertRaises(ValueError, parameters.Base.validate_ssl_options,
                          {'foo': 'bar'})

    def test_ssl_options_invalid_ssl_version(self):
        self.assertRaises(ValueError, parameters.Base.validate_ssl_options,
                          {'ssl_version': 'bar'})

    def test_virtual_host_bytes(self):
        self.assertTrue(parameters.Base.validate_virtual_host(b'foo'))

    def test_virtual_host_str(self):
        self.assertTrue(parameters.Base.validate_virtual_host('foo'))

    @unittest.skipIf(sys.version_info[0] == 3, 'No unicode obj in 3')
    def test_virtual_host_unicode(self):
        self.assertTrue(parameters.Base.validate_virtual_host(unicode('foo')))

    def test_virtual_host_invalid_int(self):
        self.assertRaises(TypeError, parameters.Base.validate_virtual_host, 10)

    def test_virtual_host_invalid_none(self):
        self.assertRaises(TypeError, parameters.Base.validate_virtual_host,
                          None)


class ParametersTests(unittest.TestCase):

    def setUp(self):
        creds = credentials.PlainCredentials('foo', 'bar')
        self.parameters = parameters.Parameters('qux', 5673, 'corgie', creds,
                                                200, 32768, 120, False, None,
                                                5, 3, 10, 'en_UK', True)

    def test_repr(self):
        self.assertEqual(repr(self.parameters),
                         '<Parameters host=qux port=5673 virtual_host=corgie '
                         'ssl=False>')

    def test_scheme(self):
        self.assertFalse(self.parameters.ssl)

    def test_host(self):
        self.assertEqual(self.parameters.host, 'qux')

    def test_port(self):
        self.assertEqual(self.parameters.port, 5673)

    def test_virtual_host(self):
        self.assertEqual(self.parameters.virtual_host, 'corgie')

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

    def test_locale(self):
        self.assertEqual(self.parameters.locale, 'en_UK')

    def test_backpressure_detection(self):
        self.assertTrue(self.parameters.backpressure_detection)


class ParametersSSLTests(unittest.TestCase):

    def setUp(self):
        self.parameters = parameters.Parameters('qux', ssl=True,
                                                ssl_options= {'ssl_version': 1})

    def test_repr(self):
        self.assertEqual(repr(self.parameters),
                         '<Parameters host=qux port=5671 virtual_host=/ '
                         'ssl=True>')

    def test_scheme(self):
        self.assertTrue(self.parameters.ssl)

    def test_host(self):
        self.assertEqual(self.parameters.host, 'qux')

    def test_port(self):
        self.assertEqual(self.parameters.port, 5671)

    def test_credentials(self):
        self.assertIsInstance(self.parameters.credentials,
                              credentials.PlainCredentials)

    def test_credentials_username(self):
        self.assertEqual(self.parameters.credentials.username, 'guest')

    def test_credentials_password(self):
        self.assertEqual(self.parameters.credentials.password, 'guest')

    def test_ssl_options_ssl_version(self):
        self.assertEqual(self.parameters.ssl_options['ssl_version'], 1)


class ParametersDefaultTests(unittest.TestCase):

    def setUp(self):
        self.parameters = parameters.Parameters()

    def test_scheme(self):
        self.assertFalse(self.parameters.ssl)

    def test_host(self):
        self.assertEqual(self.parameters.host, 'localhost')

    def test_port(self):
        self.assertEqual(self.parameters.port, 5672)

    def test_virtual_host(self):
        self.assertEqual(self.parameters.virtual_host, '/')

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

    def test_locale(self):
        self.assertEqual(self.parameters.locale, 'en_US')

    def test_backpressure_detection(self):
        self.assertFalse(self.parameters.backpressure_detection)


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

    def test_locale(self):
        self.assertEqual(self.parameters.locale, 'en_US')

    def test_backpressure_detection(self):
        self.assertFalse(self.parameters.backpressure_detection)


class AMQPOptionsTests(unittest.TestCase):

    URL = 'amqp://foo:bar@qux:5673/corgie?heartbeat_interval=120&' \
          'connection_attempts=5&channel_max=200&frame_max=32768&' \
          'locale=en_UK&retry_delay=3&socket_timeout=10&' \
          'backpressure_detection=t'

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

    def test_locale(self):
        self.assertEqual(self.parameters.locale, 'en_UK')

    def test_backpressure_detection(self):
        self.assertTrue(self.parameters.backpressure_detection)


class AMQPSOptionsTests(unittest.TestCase):

    URL = 'amqps://localhost/%2f?ssl=t&ssl_options=%7B%27ssl_version%27%3A+1%' \
          '7D&backpressure_detection=f'

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
        self.assertEqual(self.parameters.ssl_options['ssl_version'], 1)

    def test_backpressure_detection(self):
        self.assertFalse(self.parameters.backpressure_detection)
