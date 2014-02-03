"""
Connection parameters classes for validating the options passed to a connection
when creating it.

"""
from pamqp import specification
import ssl

from pika.connection import credentials as creds
from pika import exceptions
from pika import utils


class Base(object):
    """Base connection parameters class definition

    """
    backpressure_detection = False
    connection_attempts = 1
    channel_max = 0
    frame_max = specification.FRAME_MAX_SIZE
    heartbeat_interval = 0
    host = 'localhost'
    locale = 'en_US'
    password = 'guest'
    port = 5672
    retry_delay = 2.0
    socket_timeout = 0.25
    ssl = False
    ssl_options = dict({})
    username = 'guest'
    virtual_host = '/'

    VALID_SSL_OPTIONS = ['keyfile', 'certfile', 'server_side', 'cert_reqs',
                         'ssl_version', 'ca_certs', 'do_handshake_on_connect',
                         'suppress_ragged_eofs', 'ciphers']

    def __repr__(self):
        """Represent the info about the instance.

        :rtype: str

        """
        return ('<%s host=%s port=%s virtual_host=%s ssl=%s>' %
                (self.__class__.__name__, self.host, self.port,
                 self.virtual_host, self.ssl))

    def plain_credentials(self):
        """Return a plain credentials object for the specified username and
        password.

        :rtype: pika_credentials.PlainCredentials

        """
        return creds.PlainCredentials(self.username, self.password)

    @staticmethod
    def validate_backpressure(value):
        """Validate that the backpressure detection option is a bool.

        :param bool backpressure_detection: The backpressure detection value
        :rtype: bool
        :raises: TypeError

        """
        if not isinstance(value, bool):
            raise TypeError('backpressure detection must be a bool')
        return True

    @staticmethod
    def validate_channel_max(value):
        """Validate that the channel_max value is an int

        :param int value: The value to validate
        :rtype: bool
        :raises: TypeError
        :raises: ValueError

        """
        if not isinstance(value, int):
            raise TypeError('channel_max must be an int')
        if not 0 < value <= 65535:
            raise ValueError('channel_max must be > 0 and <= 65535')
        return True

    @staticmethod
    def validate_connection_attempts(value):
        """Validate that the channel_max value is an int

        :param int value: The value to validate
        :rtype: bool
        :raises: TypeError
        :raises: ValueError

        """
        if not isinstance(value, int):
            raise TypeError('connection_attempts must be an int')
        if value < 1:
            raise ValueError('connection_attempts must be None or > 0')
        return True

    @staticmethod
    def validate_credentials(value):
        """Validate the credentials passed in are using a valid object type.

        :param pika.credentials.Credentials value: Credentials to validate
        :rtype: bool
        :raises: TypeError

        """
        for credential_type in creds.VALID_TYPES:
            if isinstance(value, credential_type):
                return True
        raise TypeError('Credentials must be an object of type: %r' %
                        creds.VALID_TYPES)

    @staticmethod
    def validate_frame_max(value):
        """Validate that the frame_max value is an int and does not exceed
         the maximum frame size and is not less than the frame min size.

        :param int value: The value to validate
        :rtype: bool
        :raises: TypeError
        :raises: ValueError

        """
        if not isinstance(value, int):
            raise TypeError('frame_max must be an int')

        if (not specification.FRAME_MIN_SIZE <=
            value <= specification.FRAME_MAX_SIZE):
            raise ValueError('Frame size must be >= %s and <= %s, not %s' %
                             (specification.FRAME_MIN_SIZE,
                              specification.FRAME_MAX_SIZE,
                              value))
        return True

    @staticmethod
    def validate_heartbeat_interval(value):
        """Validate that the heartbeat_interval value is an int

        :param int value: The value to validate
        :rtype: bool
        :raises: TypeError
        :raises: ValueError

        """
        if not isinstance(value, int):
            raise TypeError('heartbeat must be an int')
        if value < 0:
            raise ValueError('heartbeat_interval must >= 0')
        return True

    @staticmethod
    def validate_host(value):
        """Validate that the host value is an str

        :param bytes|str|unicode value: The value to validate
        :rtype: bool
        :raises: TypeError

        """
        if not utils.is_string(value):
            raise TypeError('host must be bytes, str, or unicode')
        return True

    @staticmethod
    def validate_locale(value):
        """Validate that the locale value is an str

        :param bytes|str|unicode value: The value to validate
        :rtype: bool
        :raises: TypeError

        """
        if not utils.is_string(value):
            raise TypeError('locale must be bytes, str, or unicode')
        return True

    @staticmethod
    def validate_port(value):
        """Validate that the port value is an int

        :param int value: The value to validate
        :rtype: bool
        :raises: TypeError

        """
        if not isinstance(value, int):
            raise TypeError('port must be an int')
        return True

    @staticmethod
    def validate_retry_delay(value):
        """Validate that the retry_delay value is an int or float

        :param int|float value: The value to validate
        :rtype: bool
        :raises: TypeError

        """
        if not any([isinstance(value, int),
                    isinstance(value, float)]):
            raise TypeError('retry_delay must be a float or int')
        return True

    @staticmethod
    def validate_socket_timeout(value):
        """Validate that the socket_timeout value is an int or float

        :param int|float socket_timeout: The value to validate
        :rtype: bool
        :raises: TypeError

        """
        if not any([isinstance(value, int),
                    isinstance(value, float)]):
            raise TypeError('socket_timeout must be a float or int')
        if not value > 0:
            raise ValueError('socket_timeout must be > 0')
        return True

    @staticmethod
    def validate_ssl(value):
        """Validate the SSL toggle is a bool

        :param bool value: The SSL enabled/disabled value
        :rtype: bool
        :raises: TypeError

        """
        if not isinstance(value, bool):
            raise TypeError('ssl must be a bool')
        return True

    @staticmethod
    def validate_ssl_options(values):
        """Validate the SSL options value is a dictionary.

        :param dict|None values: SSL Options to validate
        :rtype: bool
        :raises: TypeError
        :raises: ValueError

        """
        if values is None:
            return True

        if not isinstance(values, dict):
            raise TypeError('ssl_options must be either None or dict')

        for key in values.keys():
            if key not in Base.VALID_SSL_OPTIONS:
                raise ValueError('%s is not a valid SSL option' % key)

        if 'ssl_version' in values:
            if values['ssl_version'] not in [ssl.PROTOCOL_SSLv2,
                                             ssl.PROTOCOL_SSLv23,
                                             ssl.PROTOCOL_SSLv3,
                                             ssl.PROTOCOL_TLSv1]:
                raise ValueError('ssl_version "%s" is not valid' %
                                 values['ssl_version'])
        return True

    @staticmethod
    def validate_virtual_host(value):
        """Validate that the virtual_host value is an str

        :param bytes|str|unicode value: The value to validate
        :rtype: bool
        :raises: TypeError

        """
        if not utils.is_string(value):
            raise TypeError('virtual_host must be bytes, str, or unicode')
        return True


class Parameters(Base):
    """Connection parameters object that is passed into the connection adapter
    upon construction.

    :param str host: Hostname or IP Address to connect to
    :param int port: TCP port to connect to
    :param str virtual_host: RabbitMQ virtual host to use
    :param pika.credentials.Credentials credentials: auth credentials
    :param int channel_max: Maximum number of channels to allow
    :param int frame_max: The maximum byte size for an AMQP frame
    :param int heartbeat_interval: How often to send heartbeats
    :param bool ssl: Enable SSL
    :param dict ssl_options: Arguments passed to ssl.wrap_socket as
    :param int connection_attempts: Maximum number of retry attempts
    :param int|float retry_delay: Time to wait in seconds, before the next
    :param int|float socket_timeout: Use for high latency networks
    :param str locale: Set the locale value
    :param bool backpressure_detection: Toggle backpressure detection

    """
    def __init__(self,
                 host=None,
                 port=None,
                 virtual_host=None,
                 credentials=None,
                 channel_max=None,
                 frame_max=None,
                 heartbeat_interval=None,
                 ssl=None,
                 ssl_options=None,
                 connection_attempts=None,
                 retry_delay=None,
                 socket_timeout=None,
                 locale=None,
                 backpressure_detection=None):
        """Create a new ConnectionParameters instance.

        :param str host: Hostname or IP Address to connect to
        :param int port: TCP port to connect to
        :param str virtual_host: RabbitMQ virtual host to use
        :param pika.credentials.Credentials credentials: auth credentials
        :param int channel_max: Maximum number of channels to allow
        :param int frame_max: The maximum byte size for an AMQP frame
        :param int heartbeat_interval: How often to send heartbeats
        :param bool ssl: Enable SSL
        :param dict ssl_options: Arguments passed to ssl.wrap_socket
        :param int connection_attempts: Maximum number of retry attempts
        :param int|float retry_delay: Time to wait in seconds, before the next
        :param int|float socket_timeout: Use for high latency networks
        :param str locale: Set the locale value
        :param bool backpressure_detection: Toggle backpressure detection

        """
        super(Parameters, self).__init__()

        # If credentials were passed in, validate and assign them
        if credentials and self.validate_credentials(credentials):
            self.credentials = credentials

        # Fallback to default credentials
        else:
            self.credentials = self.plain_credentials()

        # Assign the values
        if host and self.validate_host(host):
            self.host = host

        if port is not None and self.validate_port(port):
            self.port = port

        if virtual_host and self.validate_host(virtual_host):
            self.virtual_host = virtual_host

        if credentials and self.validate_credentials(credentials):
            self.credentials = credentials

        if channel_max is not None and self.validate_channel_max(channel_max):
            self.channel_max = channel_max

        if frame_max is not None and self.validate_frame_max(frame_max):
            self.frame_max = frame_max

        if locale and self.validate_locale(locale):
            self.locale = locale

        if (heartbeat_interval is not None and
                self.validate_heartbeat_interval(heartbeat_interval)):
            self.heartbeat = heartbeat_interval

        if ssl is not None and self.validate_ssl(ssl):
            self.ssl = ssl

        if ssl_options and self.validate_ssl_options(ssl_options):
            self.ssl_options = ssl_options or dict()

        if (connection_attempts is not None and
                self.validate_connection_attempts(connection_attempts)):
            self.connection_attempts = connection_attempts

        if retry_delay is not None and self.validate_retry_delay(retry_delay):
            self.retry_delay = retry_delay

        if (socket_timeout is not None and
                self.validate_socket_timeout(socket_timeout)):
            self.socket_timeout = socket_timeout

        if (backpressure_detection is not None and
                self.validate_backpressure(backpressure_detection)):
            self.backpressure_detection = backpressure_detection


class URLParameters(Base):
    """Connect to RabbitMQ via an AMQP URL in the format::

         amqp://username:password@host:port/<virtual_host>[?query-string]

    Ensure that the virtual host is URI encoded when specified. For example if
    you are using the default "/" virtual host, the value should be `%2f`.

    Valid query string values are:

        - backpressure_detection:
            Toggle backpressure detection, possible values are `t` or `f`
        - channel_max:
            Override the default maximum channel count value
        - connection_attempts:
            Specify how many times pika should try and reconnect before it gives up
        - frame_max:
            Override the default maximum frame size for communication
        - heartbeat_interval:
            Specify the number of seconds between heartbeat frames to ensure that
            the link between RabbitMQ and your application is up
        - locale:
            Override the default `en_US` locale value
        - ssl:
            Toggle SSL, possible values are `t`, `f`
        - ssl_options:
            Arguments passed to :meth:`ssl.wrap_socket`
        - retry_delay:
            The number of seconds to sleep before attempting to connect on
            connection failure.
        - socket_timeout:
            Override low level socket timeout value

    :param str url: The AMQP URL to connect to

    """
    DEFAULT_PORT = 5672
    DEFAULT_SSL_PORT = 5671
    DEFAULT_VIRTUAL_HOST = '/'

    def __init__(self, url):

        """Create a new URLParameters instance.

        :param str url: The URL value

        """
        super(URLParameters, self).__init__()
        parts = utils.urlparse(url)

        # Handle the Protocol scheme, changing to HTTPS so urlparse doesnt barf
        if parts.scheme == 'amqps':
            self.ssl = True

        if self.validate_host(parts.hostname):
            self.host = parts.hostname

        if parts.port and self.validate_port(parts.port):
            self.port = parts.port
        else:
            self.port = (self.DEFAULT_PORT if not self.ssl else
                         self.DEFAULT_SSL_PORT)

        # Handle authentication credentials
        if parts.username:
            self.username = parts.username
        if parts.password:
            self.password = parts.password
        self.credentials = self.plain_credentials()

        # Get the Virtual Host
        if len(parts.path) <= 1:
            self.virtual_host = self.DEFAULT_VIRTUAL_HOST
        else:
            path_parts = parts.path.split('/')
            virtual_host = utils.unquote(path_parts[1])
            if self.validate_virtual_host(virtual_host):
                self.virtual_host = virtual_host

        # Handle query string values, validating and assigning them
        values = utils.parse_qs(parts.query)

        # Cast the various numeric values to the appropriate values
        for key in values.keys():
            # Always reassign the first list item in query values
            values[key] = values[key].pop(0)
            if values[key].isdigit():
                values[key] = int(values[key])
            else:
                try:
                    values[key] = float(values[key])
                except ValueError:
                    pass

        if 'backpressure_detection' in values:
            if values['backpressure_detection'] == 't':
                self.backpressure_detection = True
            elif values['backpressure_detection'] == 'f':
                self.backpressure_detection = False
            else:
                raise ValueError('Invalid backpressure_detection value: %s' %
                                 values['backpressure_detection'])

        if ('channel_max' in values and
                self.validate_channel_max(values['channel_max'])):
            self.channel_max = values['channel_max']

        if ('connection_attempts' in values and
                self.validate_connection_attempts(values['connection_attempts'])):
            self.connection_attempts = values['connection_attempts']

        if ('frame_max' in values and
            self.validate_frame_max(values['frame_max'])):
            self.frame_max = values['frame_max']

        if ('heartbeat_interval' in values and
            self.validate_heartbeat_interval(values['heartbeat_interval'])):
            self.heartbeat = values['heartbeat_interval']

        if ('locale' in values and
            self.validate_locale(values['locale'])):
            self.locale = values['locale']

        if ('retry_delay' in values and
            self.validate_retry_delay(values['retry_delay'])):
            self.retry_delay = values['retry_delay']

        if ('socket_timeout' in values and
            self.validate_socket_timeout(values['socket_timeout'])):
            self.socket_timeout = values['socket_timeout']

        if 'ssl_options' in values:
            options = ast.literal_eval(values['ssl_options'])
            if self.validate_ssl_options(options):
                self.ssl_options = options
