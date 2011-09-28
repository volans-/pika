"""specification.py

Auto-generated AMQP Support Module

WARNING: DO NOT EDIT. To Generate run tools/codegen.py

For copyright and licensing please refer to COPYING.

"""

__date__ = "2011-09-28"
__author__ = "codegen.py"

from pika import codec

# AMQP Protocol Version
AMQP_VERSION = (0, 9, 1)

# RabbitMQ Defaults
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5672
DEFAULT_USER = "guest"
DEFAULT_PASS = "guest"

# AMQP Constants
AMQP_FRAME_METHOD = 1
AMQP_FRAME_HEADER = 2
AMQP_FRAME_BODY = 3
AMQP_FRAME_HEARTBEAT = 8
AMQP_FRAME_MIN_SIZE = 4096
AMQP_FRAME_END = 206
# Indicates that the method completed successfully. This reply code is reserved
# for future use - the current protocol design does not use positive
# confirmation and reply codes are sent only in case of an error.
AMQP_REPLY_SUCCESS = 200

# AMQP data types
AMQP_DATA_TYPES = ["bit",
                   "long",
                   "longlong",
                   "longstr",
                   "octet",
                   "short",
                   "shortstr",
                   "table",
                   "timestamp"]

# AMQP domains
AMQP_DOMAINS = {"channel-id": "longstr",
                "class-id": "short",
                "consumer-tag": "shortstr",
                "delivery-tag": "longlong",
                "destination": "shortstr",
                "duration": "longlong",
                "exchange-name": "shortstr",
                "method-id": "short",
                "no-ack": "bit",
                "no-local": "bit",
                "offset": "longlong",
                "path": "shortstr",
                "peer-properties": "table",
                "queue-name": "shortstr",
                "redelivered": "bit",
                "reference": "longstr",
                "reject-code": "short",
                "reject-text": "shortstr",
                "reply-code": "short",
                "reply-text": "shortstr",
                "security-token": "longstr"}

# Other constants
DEPRECATION_WARNING = "This command is deprecated in AMQP 0-9-1"


class Frame(object):
    """Base Class for AMQP Methods which specifies the encoding and decoding
    behavior.

    """
    attributes = list()
    id = 0
    index = 0
    name = 'Frame'

    def demarshal(self, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param data: The binary encoded method data
        :type data: str

        """
        offset = 0
        processing_bitset = False
        for argument in self.attributes:

            data_type = getattr(self.__class__, argument)

            if offset == 7 and processing_bitset:
                data = data[1:]
                offset = 0

            if processing_bitset and data_type != 'bit':
                offset = 0
                processing_bitset = False
                data = data[1:]

            consumed, value = codec.decode.by_type(data, data_type, offset)

            if data_type == 'bit':
                offset += 1
                processing_bitset = True

            setattr(self, argument, value)
            if consumed:
                data = data[consumed:]

    def marshal(self):
        """
        Dynamically encode the frame by taking the list of attributes and
        encode them item by item getting the value form the object attribute
        and the data type from the class attribute.

        :returns: unicode

        """
        output = list()
        for argument in self.attributes:
            output.append(codec.encode.by_type(getattr(self,
                                                       argument),
                                               getattr(self.__class__,
                                                       argument)))
        return u''.join(output)



class PropertiesBase(object):
    """Provide a base object that marshals and demarshals the Basic.Properties
    object values.

    """

    attributes = list()
    flags = dict()
    name = 'PropertiesBase'

    def demarshal(self, flags, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param flags: Flags that indicate if the data has the given property
        :type flags: int
        :param data: The binary encoded method data
        :type data: unicode

        """
        flag_values = getattr(self.__class__, 'flags')
        for attribute in self.attributes:
            if flags & flag_values[attribute]:
                attribute = attribute.replace('-', '_')
                data_type = getattr(self.__class__, attribute)
                consumed, value = codec.decode.by_type(data, data_type)
                setattr(self, attribute, value)
                data = data[consumed:]


# AMQP Errors
class AMQPContentTooLarge(Warning):
    """
    The client attempted to transfer content larger than the server could
    accept at the present time. The client may retry at a later time.

    """
    name = "CONTENT-TOO-LARGE"
    value = 311


class AMQPNoRoute(Warning):
    """
    Undocumented AMQP Soft Error

    """
    name = "NO-ROUTE"
    value = 312


class AMQPNoConsumers(Warning):
    """
    When the exchange cannot deliver to a consumer when the immediate flag is
    set. As a result of pending data on the queue or the absence of any
    consumers of the queue.

    """
    name = "NO-CONSUMERS"
    value = 313


class AMQPAccessRefused(Warning):
    """
    The client attempted to work with a server entity to which it has no access
    due to security settings.

    """
    name = "ACCESS-REFUSED"
    value = 403


class AMQPNotFound(Warning):
    """
    The client attempted to work with a server entity that does not exist.

    """
    name = "NOT-FOUND"
    value = 404


class AMQPResourceLocked(Warning):
    """
    The client attempted to work with a server entity to which it has no access
    because another client is working with it.

    """
    name = "RESOURCE-LOCKED"
    value = 405


class AMQPPreconditionFailed(Warning):
    """
    The client requested a method that was not allowed because some
    precondition failed.

    """
    name = "PRECONDITION-FAILED"
    value = 406


class AMQPConnectionForced(Exception):
    """
    An operator intervened to close the connection for some reason. The client
    may retry at some later date.

    """
    name = "CONNECTION-FORCED"
    value = 320


class AMQPInvalidPath(Exception):
    """
    The client tried to work with an unknown virtual host.

    """
    name = "INVALID-PATH"
    value = 402


class AMQPFrameError(Exception):
    """
    The sender sent a malformed frame that the recipient could not decode. This
    strongly implies a programming error in the sending peer.

    """
    name = "FRAME-ERROR"
    value = 501


class AMQPSyntaxError(Exception):
    """
    The sender sent a frame that contained illegal values for one or more
    fields. This strongly implies a programming error in the sending peer.

    """
    name = "SYNTAX-ERROR"
    value = 502


class AMQPCommandInvalid(Exception):
    """
    The client sent an invalid sequence of frames, attempting to perform an
    operation that was considered invalid by the server. This usually implies a
    programming error in the client.

    """
    name = "COMMAND-INVALID"
    value = 503


class AMQPChannelError(Exception):
    """
    The client attempted to work with a channel that had not been correctly
    opened. This most likely indicates a fault in the client layer.

    """
    name = "CHANNEL-ERROR"
    value = 504


class AMQPUnexpectedFrame(Exception):
    """
    The peer sent a frame that was not expected, usually in the context of a
    content header and body.  This strongly indicates a fault in the peer's
    content processing.

    """
    name = "UNEXPECTED-FRAME"
    value = 505


class AMQPResourceError(Exception):
    """
    The server could not complete the method because it lacked sufficient
    resources. This may be due to the client creating too many of some type of
    entity.

    """
    name = "RESOURCE-ERROR"
    value = 506


class AMQPNotAllowed(Exception):
    """
    The client tried to work with some entity in a manner that is prohibited by
    the server, due to security settings or by some other criteria.

    """
    name = "NOT-ALLOWED"
    value = 530


class AMQPNotImplemented(Exception):
    """
    The client tried to use functionality that is not implemented in the
    server.

    """
    name = "NOT-IMPLEMENTED"
    value = 540


class AMQPInternalError(Exception):
    """
    The server could not complete the method because of an internal error. The
    server may require intervention by an operator in order to resume normal
    operations.

    """
    name = "INTERNAL-ERROR"
    value = 541


# AMQP Error code to class mapping
AMQP_ERRORS = {320: AMQPConnectionForced,
               505: AMQPUnexpectedFrame,
               502: AMQPSyntaxError,
               503: AMQPCommandInvalid,
               530: AMQPNotAllowed,
               504: AMQPChannelError,
               402: AMQPInvalidPath,
               403: AMQPAccessRefused,
               404: AMQPNotFound,
               405: AMQPResourceLocked,
               406: AMQPPreconditionFailed,
               311: AMQPContentTooLarge,
               312: AMQPNoRoute,
               313: AMQPNoConsumers,
               506: AMQPResourceError,
               540: AMQPNotImplemented,
               541: AMQPInternalError,
               501: AMQPFrameError}

# AMQP Classes and Methods


class Connection(object):
    """Work with socket connections

    The connection class provides methods for a client to establish a network
    connection to a server, and for both peers to operate the connection
    thereafter.

    """
    # AMQP Class Number and Mapping Index
    id = 10
    index = 0x000A0000

    class Start(Frame):
        """Start connection negotiation

        This method starts the connection negotiation process by telling the
        client the protocol version that the server proposes, along with a list
        of security mechanisms which the client can use for authentication.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x000A000A
        name = 'Connection.Start'

        # AMQP Method Attributes
        attributes = ["version_major",
                      "version_minor",
                      "server_properties",
                      "mechanisms",
                      "locales"]

        # Class Attribute Types
        version_major = "octet"
        version_minor = "octet"
        server_properties = "table"
        mechanisms = "longstr"
        locales = "longstr"

        def __init__(self, version_major=0, version_minor=9,
                     server_properties=None, mechanisms=u'PLAIN',
                     locales=u'en_US'):
            """Initialize the Connection.Start class

            :param version_major: Protocol major version
            :type version_major: int
            :param version_minor: Protocol minor version
            :type version_minor: int
            :param server_properties: Server properties
            :type server_properties: dict
            :param mechanisms: Available security mechanisms
            :type mechanisms: str
            :param locales: Available message locales
            :type locales: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Connection.StartOk]

            # Protocol major version
            self.version_major = version_major

            # Protocol minor version
            self.version_minor = version_minor

            # Server properties
            self.server_properties = server_properties

            # Available security mechanisms
            self.mechanisms = mechanisms

            # Available message locales
            self.locales = locales

    class StartOk(Frame):
        """Select security mechanism and locale

        This method selects a SASL security mechanism.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x000A000B
        name = 'Connection.StartOk'

        # AMQP Method Attributes
        attributes = ["client_properties",
                      "mechanism",
                      "response",
                      "locale"]

        # Class Attribute Types
        client_properties = "table"
        mechanism = "shortstr"
        response = "longstr"
        locale = "shortstr"

        def __init__(self, client_properties=None, mechanism=u'PLAIN',
                     response=None, locale=u'en_US'):
            """Initialize the Connection.StartOk class

            :param client_properties: Client properties
            :type client_properties: dict
            :param mechanism: Selected security mechanism
            :type mechanism: str
            :param response: Security response data
            :type response: str
            :param locale: Selected message locale
            :type locale: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Client properties
            self.client_properties = client_properties

            # Selected security mechanism
            self.mechanism = mechanism

            # Security response data
            self.response = response

            # Selected message locale
            self.locale = locale

    class Secure(Frame):
        """Security mechanism challenge

        The SASL protocol works by exchanging challenges and responses until
        both peers have received sufficient information to authenticate each
        other. This method challenges the client to provide more information.

        """
        # AMQP Method Number and Mapping Index
        id = 20
        index = 0x000A0014
        name = 'Connection.Secure'

        # AMQP Method Attributes
        attributes = ["challenge"]

        # Class Attribute Types
        challenge = "longstr"

        def __init__(self, challenge=None):
            """Initialize the Connection.Secure class

            :param challenge: Security challenge data
            :type challenge: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Connection.SecureOk]

            # Security challenge data
            self.challenge = challenge

    class SecureOk(Frame):
        """Security mechanism response

        This method attempts to authenticate, passing a block of SASL data for
        the security mechanism at the server side.

        """
        # AMQP Method Number and Mapping Index
        id = 21
        index = 0x000A0015
        name = 'Connection.SecureOk'

        # AMQP Method Attributes
        attributes = ["response"]

        # Class Attribute Types
        response = "longstr"

        def __init__(self, response=None):
            """Initialize the Connection.SecureOk class

            :param response: Security response data
            :type response: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Security response data
            self.response = response

    class Tune(Frame):
        """Propose connection tuning parameters

        This method proposes a set of connection configuration values to the
        client. The client can accept and/or adjust these.

        """
        # AMQP Method Number and Mapping Index
        id = 30
        index = 0x000A001E
        name = 'Connection.Tune'

        # AMQP Method Attributes
        attributes = ["channel_max",
                      "frame_max",
                      "heartbeat"]

        # Class Attribute Types
        channel_max = "short"
        frame_max = "long"
        heartbeat = "short"

        def __init__(self, channel_max=0, frame_max=0, heartbeat=0):
            """Initialize the Connection.Tune class

            :param channel_max: Proposed maximum channels
            :type channel_max: int
            :param frame_max: Proposed maximum frame size
            :type frame_max: int/long
            :param heartbeat: Desired heartbeat delay
            :type heartbeat: int

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Connection.TuneOk]

            # Proposed maximum channels
            self.channel_max = channel_max

            # Proposed maximum frame size
            self.frame_max = frame_max

            # Desired heartbeat delay
            self.heartbeat = heartbeat

    class TuneOk(Frame):
        """Negotiate connection tuning parameters

        This method sends the client's connection tuning parameters to the
        server. Certain fields are negotiated, others provide capability
        information.

        """
        # AMQP Method Number and Mapping Index
        id = 31
        index = 0x000A001F
        name = 'Connection.TuneOk'

        # AMQP Method Attributes
        attributes = ["channel_max",
                      "frame_max",
                      "heartbeat"]

        # Class Attribute Types
        channel_max = "short"
        frame_max = "long"
        heartbeat = "short"

        def __init__(self, channel_max=0, frame_max=0, heartbeat=0):
            """Initialize the Connection.TuneOk class

            :param channel_max: Negotiated maximum channels
            :type channel_max: int
            :param frame_max: Negotiated maximum frame size
            :type frame_max: int/long
            :param heartbeat: Desired heartbeat delay
            :type heartbeat: int

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Negotiated maximum channels
            self.channel_max = channel_max

            # Negotiated maximum frame size
            self.frame_max = frame_max

            # Desired heartbeat delay
            self.heartbeat = heartbeat

    class Open(Frame):
        """Open connection to virtual host

        This method opens a connection to a virtual host, which is a collection
        of resources, and acts to separate multiple application domains within
        a server. The server may apply arbitrary limits per virtual host, such
        as the number of each type of entity that may be used, per connection
        and/or in total.

        """
        # AMQP Method Number and Mapping Index
        id = 40
        index = 0x000A0028
        name = 'Connection.Open'

        # AMQP Method Attributes
        attributes = ["virtual_host",
                      "capabilities",
                      "insist"]

        # Class Attribute Types
        virtual_host = "shortstr"
        capabilities = "shortstr"
        insist = "bit"

        def __init__(self, virtual_host=u'/', capabilities=None, insist=False):
            """Initialize the Connection.Open class

            :param virtual_host: Virtual host name
            :type virtual_host: str
            :param capabilities: Deprecated
            :type capabilities: str
            :param insist: Deprecated
            :type insist: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Connection.OpenOk]

            # Virtual host name
            self.virtual_host = virtual_host

            # Deprecated
            self.capabilities = capabilities

            # Deprecated
            self.insist = insist

    class OpenOk(Frame):
        """Signal that connection is ready

        This method signals to the client that the connection is ready for use.

        """
        # AMQP Method Number and Mapping Index
        id = 41
        index = 0x000A0029
        name = 'Connection.OpenOk'

        # AMQP Method Attributes
        attributes = ["known_hosts"]

        # Class Attribute Types
        known_hosts = "shortstr"

        def __init__(self, known_hosts=None):
            """Initialize the Connection.OpenOk class

            :param known_hosts: Deprecated
            :type known_hosts: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Deprecated
            self.known_hosts = known_hosts

    class Close(Frame):
        """Request a connection close

        This method indicates that the sender wants to close the connection.
        This may be due to internal conditions (e.g. a forced shut-down) or due
        to an error handling a specific method, i.e. an exception. When a close
        is due to an exception, the sender provides the class and method id of
        the method which caused the exception.

        """
        # AMQP Method Number and Mapping Index
        id = 50
        index = 0x000A0032
        name = 'Connection.Close'

        # AMQP Method Attributes
        attributes = ["reply_code",
                      "reply_text",
                      "class_id",
                      "method_id"]

        # Class Attribute Types
        reply_code = "short"
        reply_text = "shortstr"
        class_id = "short"
        method_id = "short"

        def __init__(self, reply_code=None, reply_text=None, class_id=None,
                     method_id=None):
            """Initialize the Connection.Close class

            :param reply_code: Reply code from server
            :type reply_code: int
            :param reply_text: Localised reply text
            :type reply_text: str
            :param class_id: Failing method class
            :type class_id: int
            :param method_id: Failing method ID
            :type method_id: int

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Connection.CloseOk]

            # Reply code from server
            self.reply_code = reply_code

            # Localised reply text
            self.reply_text = reply_text

            # Failing method class
            self.class_id = class_id

            # Failing method ID
            self.method_id = method_id

    class CloseOk(Frame):
        """Confirm a connection close

        This method confirms a Connection.Close method and tells the recipient
        that it is safe to release resources for the connection and close the
        socket.

        """
        # AMQP Method Number and Mapping Index
        id = 51
        index = 0x000A0033
        name = 'Connection.CloseOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Connection.CloseOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False


class Channel(object):
    """Work with channels

    The channel class provides methods for a client to establish a channel to a
    server and for both peers to operate the channel thereafter.

    """
    # AMQP Class Number and Mapping Index
    id = 20
    index = 0x00140000

    class Open(Frame):
        """Open a channel for use

        This method opens a channel to the server.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x0014000A
        name = 'Channel.Open'

        # AMQP Method Attributes
        attributes = ["out_of_band"]

        # Class Attribute Types
        out_of_band = "shortstr"

        def __init__(self, out_of_band=None):
            """Initialize the Channel.Open class

            :param out_of_band: Protocol level field, do not use, must be zero.
            :type out_of_band: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Channel.OpenOk]

            # Protocol level field, do not use, must be zero.
            self.out_of_band = out_of_band

    class OpenOk(Frame):
        """Signal that the channel is ready

        This method signals to the client that the channel is ready for use.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x0014000B
        name = 'Channel.OpenOk'

        # AMQP Method Attributes
        attributes = ["channel_id"]

        # Class Attribute Types
        channel_id = "longstr"

        def __init__(self, channel_id=None):
            """Initialize the Channel.OpenOk class

            :param channel_id: Deprecated
            :type channel_id: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Deprecated
            self.channel_id = channel_id

    class Flow(Frame):
        """Enable/disable flow from peer

        This method asks the peer to pause or restart the flow of content data
        sent by a consumer. This is a simple flow-control mechanism that a peer
        can use to avoid overflowing its queues or otherwise finding itself
        receiving more messages than it can process. Note that this method is
        not intended for window control. It does not affect contents returned
        by Basic.Get-Ok methods.

        """
        # AMQP Method Number and Mapping Index
        id = 20
        index = 0x00140014
        name = 'Channel.Flow'

        # AMQP Method Attributes
        attributes = ["active"]

        # Class Attribute Types
        active = "bit"

        def __init__(self, active=None):
            """Initialize the Channel.Flow class

            :param active: Start/stop content frames
            :type active: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Channel.FlowOk]

            # Start/stop content frames
            self.active = active

    class FlowOk(Frame):
        """Confirm a flow method

        Confirms to the peer that a flow command was received and processed.

        """
        # AMQP Method Number and Mapping Index
        id = 21
        index = 0x00140015
        name = 'Channel.FlowOk'

        # AMQP Method Attributes
        attributes = ["active"]

        # Class Attribute Types
        active = "bit"

        def __init__(self, active=None):
            """Initialize the Channel.FlowOk class

            :param active: Current flow setting
            :type active: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Current flow setting
            self.active = active

    class Close(Frame):
        """Request a channel close

        This method indicates that the sender wants to close the channel. This
        may be due to internal conditions (e.g. a forced shut-down) or due to
        an error handling a specific method, i.e. an exception. When a close is
        due to an exception, the sender provides the class and method id of the
        method which caused the exception.

        """
        # AMQP Method Number and Mapping Index
        id = 40
        index = 0x00140028
        name = 'Channel.Close'

        # AMQP Method Attributes
        attributes = ["reply_code",
                      "reply_text",
                      "class_id",
                      "method_id"]

        # Class Attribute Types
        reply_code = "short"
        reply_text = "shortstr"
        class_id = "short"
        method_id = "short"

        def __init__(self, reply_code=None, reply_text=None, class_id=None,
                     method_id=None):
            """Initialize the Channel.Close class

            :param reply_code: Reply code from server
            :type reply_code: int
            :param reply_text: Localised reply text
            :type reply_text: str
            :param class_id: Failing method class
            :type class_id: int
            :param method_id: Failing method ID
            :type method_id: int

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Channel.CloseOk]

            # Reply code from server
            self.reply_code = reply_code

            # Localised reply text
            self.reply_text = reply_text

            # Failing method class
            self.class_id = class_id

            # Failing method ID
            self.method_id = method_id

    class CloseOk(Frame):
        """Confirm a channel close

        This method confirms a Channel.Close method and tells the recipient
        that it is safe to release resources for the channel.

        """
        # AMQP Method Number and Mapping Index
        id = 41
        index = 0x00140029
        name = 'Channel.CloseOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Channel.CloseOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False


class Exchange(object):
    """Work with exchanges

    Exchanges match and distribute messages across queues. Exchanges can be
    configured in the server or declared at runtime.

    """
    # AMQP Class Number and Mapping Index
    id = 40
    index = 0x00280000

    class Declare(Frame):
        """Verify exchange exists, create if needed

        This method creates an exchange if it does not already exist, and if
        the exchange exists, verifies that it is of the correct and expected
        class.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x0028000A
        name = 'Exchange.Declare'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "exchange",
                      "type",
                      "passive",
                      "durable",
                      "auto_delete",
                      "internal",
                      "nowait",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        exchange = "shortstr"
        type = "shortstr"
        passive = "bit"
        durable = "bit"
        auto_delete = "bit"
        internal = "bit"
        nowait = "bit"
        arguments = "table"

        def __init__(self, ticket=0, exchange=None, type=u'direct',
                     passive=False, durable=False, auto_delete=False,
                     internal=False, nowait=False, arguments={}):
            """Initialize the Exchange.Declare class

            :param ticket: Deprecated
            :type ticket: int
            :param exchange:
            :type exchange: str
            :param type: Exchange type
            :type type: str
            :param passive: Do not create exchange
            :type passive: bool
            :param durable: Request a durable exchange
            :type durable: bool
            :param auto_delete: Auto-delete when unused
            :type auto_delete: bool
            :param internal: Create internal exchange
            :type internal: bool
            :param nowait: Do not send a reply method
            :type nowait: bool
            :param arguments: Arguments for declaration
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Exchange.DeclareOk]

            # Deprecated
            self.ticket = ticket

            self.exchange = exchange

            # Exchange type
            self.type = type

            # Do not create exchange
            self.passive = passive

            # Request a durable exchange
            self.durable = durable

            # Auto-delete when unused
            self.auto_delete = auto_delete

            # Create internal exchange
            self.internal = internal

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for declaration
            self.arguments = arguments

    class DeclareOk(Frame):
        """Confirm exchange declaration

        This method confirms a Declare method and confirms the name of the
        exchange, essential for automatically-named exchanges.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x0028000B
        name = 'Exchange.DeclareOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Exchange.DeclareOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Delete(Frame):
        """Delete an exchange

        This method deletes an exchange. When an exchange is deleted all queue
        bindings on the exchange are cancelled.

        """
        # AMQP Method Number and Mapping Index
        id = 20
        index = 0x00280014
        name = 'Exchange.Delete'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "exchange",
                      "if_unused",
                      "nowait"]

        # Class Attribute Types
        ticket = "short"
        exchange = "shortstr"
        if_unused = "bit"
        nowait = "bit"

        def __init__(self, ticket=0, exchange=None, if_unused=False,
                     nowait=False):
            """Initialize the Exchange.Delete class

            :param ticket: Deprecated
            :type ticket: int
            :param exchange:
            :type exchange: str
            :param if_unused: Delete only if unused
            :type if_unused: bool
            :param nowait: Do not send a reply method
            :type nowait: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Exchange.DeleteOk]

            # Deprecated
            self.ticket = ticket

            self.exchange = exchange

            # Delete only if unused
            self.if_unused = if_unused

            # Do not send a reply method
            self.nowait = nowait

    class DeleteOk(Frame):
        """Confirm deletion of an exchange

        This method confirms the deletion of an exchange.

        """
        # AMQP Method Number and Mapping Index
        id = 21
        index = 0x00280015
        name = 'Exchange.DeleteOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Exchange.DeleteOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Bind(Frame):
        """Bind exchange to an exchange

        This method binds an exchange to an exchange.

        """
        # AMQP Method Number and Mapping Index
        id = 30
        index = 0x0028001E
        name = 'Exchange.Bind'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "destination",
                      "source",
                      "routing_key",
                      "nowait",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        destination = "shortstr"
        source = "shortstr"
        routing_key = "shortstr"
        nowait = "bit"
        arguments = "table"

        def __init__(self, ticket=0, destination=None, source=None,
                     routing_key=None, nowait=False, arguments={}):
            """Initialize the Exchange.Bind class

            :param ticket: Deprecated
            :type ticket: int
            :param destination: Name of the destination exchange to bind to
            :type destination: str
            :param source: Name of the source exchange to bind to
            :type source: str
            :param routing_key: Message routing key
            :type routing_key: str
            :param nowait: Do not send a reply method
            :type nowait: bool
            :param arguments: Arguments for binding
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Exchange.BindOk]

            # Deprecated
            self.ticket = ticket

            # Name of the destination exchange to bind to
            self.destination = destination

            # Name of the source exchange to bind to
            self.source = source

            # Message routing key
            self.routing_key = routing_key

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for binding
            self.arguments = arguments

    class BindOk(Frame):
        """Confirm bind successful

        This method confirms that the bind was successful.

        """
        # AMQP Method Number and Mapping Index
        id = 31
        index = 0x0028001F
        name = 'Exchange.BindOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Exchange.BindOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Unbind(Frame):
        """Unbind an exchange from an exchange

        This method unbinds an exchange from an exchange.

        """
        # AMQP Method Number and Mapping Index
        id = 40
        index = 0x00280028
        name = 'Exchange.Unbind'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "destination",
                      "source",
                      "routing_key",
                      "nowait",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        destination = "shortstr"
        source = "shortstr"
        routing_key = "shortstr"
        nowait = "bit"
        arguments = "table"

        def __init__(self, ticket=0, destination=None, source=None,
                     routing_key=None, nowait=False, arguments={}):
            """Initialize the Exchange.Unbind class

            :param ticket: Deprecated
            :type ticket: int
            :param destination:
            :type destination: str
            :param source:
            :type source: str
            :param routing_key: Routing key of binding
            :type routing_key: str
            :param nowait: Do not send a reply method
            :type nowait: bool
            :param arguments: Arguments of binding
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Exchange.UnbindOk]

            # Deprecated
            self.ticket = ticket

            self.destination = destination

            self.source = source

            # Routing key of binding
            self.routing_key = routing_key

            # Do not send a reply method
            self.nowait = nowait

            # Arguments of binding
            self.arguments = arguments

    class UnbindOk(Frame):
        """Confirm unbind successful

        This method confirms that the unbind was successful.

        """
        # AMQP Method Number and Mapping Index
        id = 51
        index = 0x00280033
        name = 'Exchange.UnbindOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Exchange.UnbindOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False


class Queue(object):
    """Work with queues

    Queues store and forward messages. Queues can be configured in the server
    or created at runtime. Queues must be attached to at least one exchange in
    order to receive messages from publishers.

    """
    # AMQP Class Number and Mapping Index
    id = 50
    index = 0x00320000

    class Declare(Frame):
        """Declare queue, create if needed

        This method creates or checks a queue. When creating a new queue the
        client can specify various properties that control the durability of
        the queue and its contents, and the level of sharing for the queue.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x0032000A
        name = 'Queue.Declare'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "passive",
                      "durable",
                      "exclusive",
                      "auto_delete",
                      "nowait",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        passive = "bit"
        durable = "bit"
        exclusive = "bit"
        auto_delete = "bit"
        nowait = "bit"
        arguments = "table"

        def __init__(self, ticket=0, queue=None, passive=False, durable=False,
                     exclusive=False, auto_delete=False, nowait=False,
                     arguments={}):
            """Initialize the Queue.Declare class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param passive: Do not create queue
            :type passive: bool
            :param durable: Request a durable queue
            :type durable: bool
            :param exclusive: Request an exclusive queue
            :type exclusive: bool
            :param auto_delete: Auto-delete queue when unused
            :type auto_delete: bool
            :param nowait: Do not send a reply method
            :type nowait: bool
            :param arguments: Arguments for declaration
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Queue.DeclareOk]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Do not create queue
            self.passive = passive

            # Request a durable queue
            self.durable = durable

            # Request an exclusive queue
            self.exclusive = exclusive

            # Auto-delete queue when unused
            self.auto_delete = auto_delete

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for declaration
            self.arguments = arguments

    class DeclareOk(Frame):
        """Confirms a queue definition

        This method confirms a Declare method and confirms the name of the
        queue, essential for automatically-named queues.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x0032000B
        name = 'Queue.DeclareOk'

        # AMQP Method Attributes
        attributes = ["queue",
                      "message_count",
                      "consumer_count"]

        # Class Attribute Types
        queue = "shortstr"
        message_count = "long"
        consumer_count = "long"

        def __init__(self, queue=None, message_count=None,
                     consumer_count=None):
            """Initialize the Queue.DeclareOk class

            :param queue:
            :type queue: str
            :param message_count: Number of messages in queue
            :type message_count: int/long
            :param consumer_count: Number of consumers
            :type consumer_count: int/long

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            self.queue = queue

            # Number of messages in queue
            self.message_count = message_count

            # Number of consumers
            self.consumer_count = consumer_count

    class Bind(Frame):
        """Bind queue to an exchange

        This method binds a queue to an exchange. Until a queue is bound it
        will not receive any messages. In a classic messaging model, store-and-
        forward queues are bound to a direct exchange and subscription queues
        are bound to a topic exchange.

        """
        # AMQP Method Number and Mapping Index
        id = 20
        index = 0x00320014
        name = 'Queue.Bind'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "exchange",
                      "routing_key",
                      "nowait",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        exchange = "shortstr"
        routing_key = "shortstr"
        nowait = "bit"
        arguments = "table"

        def __init__(self, ticket=0, queue=None, exchange=None,
                     routing_key=None, nowait=False, arguments={}):
            """Initialize the Queue.Bind class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param exchange: Name of the exchange to bind to
            :type exchange: str
            :param routing_key: Message routing key
            :type routing_key: str
            :param nowait: Do not send a reply method
            :type nowait: bool
            :param arguments: Arguments for binding
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Queue.BindOk]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Name of the exchange to bind to
            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for binding
            self.arguments = arguments

    class BindOk(Frame):
        """Confirm bind successful

        This method confirms that the bind was successful.

        """
        # AMQP Method Number and Mapping Index
        id = 21
        index = 0x00320015
        name = 'Queue.BindOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Queue.BindOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Purge(Frame):
        """Purge a queue

        This method removes all messages from a queue which are not awaiting
        acknowledgment.

        """
        # AMQP Method Number and Mapping Index
        id = 30
        index = 0x0032001E
        name = 'Queue.Purge'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "nowait"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        nowait = "bit"

        def __init__(self, ticket=0, queue=None, nowait=False):
            """Initialize the Queue.Purge class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param nowait: Do not send a reply method
            :type nowait: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Queue.PurgeOk]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Do not send a reply method
            self.nowait = nowait

    class PurgeOk(Frame):
        """Confirms a queue purge

        This method confirms the purge of a queue.

        """
        # AMQP Method Number and Mapping Index
        id = 31
        index = 0x0032001F
        name = 'Queue.PurgeOk'

        # AMQP Method Attributes
        attributes = ["message_count"]

        # Class Attribute Types
        message_count = "long"

        def __init__(self, message_count=None):
            """Initialize the Queue.PurgeOk class

            :param message_count:
            :type message_count: int/long

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            self.message_count = message_count

    class Delete(Frame):
        """Delete a queue

        This method deletes a queue. When a queue is deleted any pending
        messages are sent to a dead-letter queue if this is defined in the
        server configuration, and all consumers on the queue are cancelled.

        """
        # AMQP Method Number and Mapping Index
        id = 40
        index = 0x00320028
        name = 'Queue.Delete'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "if_unused",
                      "if_empty",
                      "nowait"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        if_unused = "bit"
        if_empty = "bit"
        nowait = "bit"

        def __init__(self, ticket=0, queue=None, if_unused=False,
                     if_empty=False, nowait=False):
            """Initialize the Queue.Delete class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param if_unused: Delete only if unused
            :type if_unused: bool
            :param if_empty: Delete only if empty
            :type if_empty: bool
            :param nowait: Do not send a reply method
            :type nowait: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Queue.DeleteOk]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Delete only if unused
            self.if_unused = if_unused

            # Delete only if empty
            self.if_empty = if_empty

            # Do not send a reply method
            self.nowait = nowait

    class DeleteOk(Frame):
        """Confirm deletion of a queue

        This method confirms the deletion of a queue.

        """
        # AMQP Method Number and Mapping Index
        id = 41
        index = 0x00320029
        name = 'Queue.DeleteOk'

        # AMQP Method Attributes
        attributes = ["message_count"]

        # Class Attribute Types
        message_count = "long"

        def __init__(self, message_count=None):
            """Initialize the Queue.DeleteOk class

            :param message_count:
            :type message_count: int/long

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            self.message_count = message_count

    class Unbind(Frame):
        """Unbind a queue from an exchange

        This method unbinds a queue from an exchange.

        """
        # AMQP Method Number and Mapping Index
        id = 50
        index = 0x00320032
        name = 'Queue.Unbind'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "exchange",
                      "routing_key",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        exchange = "shortstr"
        routing_key = "shortstr"
        arguments = "table"

        def __init__(self, ticket=0, queue=None, exchange=None,
                     routing_key=None, arguments={}):
            """Initialize the Queue.Unbind class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param exchange:
            :type exchange: str
            :param routing_key: Routing key of binding
            :type routing_key: str
            :param arguments: Arguments of binding
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Queue.UnbindOk]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            self.exchange = exchange

            # Routing key of binding
            self.routing_key = routing_key

            # Arguments of binding
            self.arguments = arguments

    class UnbindOk(Frame):
        """Confirm unbind successful

        This method confirms that the unbind was successful.

        """
        # AMQP Method Number and Mapping Index
        id = 51
        index = 0x00320033
        name = 'Queue.UnbindOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Queue.UnbindOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False


class Basic(object):
    """Work with basic content

    The Basic class provides methods that support an industry-standard
    messaging model.

    """
    # AMQP Class Number and Mapping Index
    id = 60
    index = 0x003C0000

    class Qos(Frame):
        """Specify quality of service

        This method requests a specific quality of service. The QoS can be
        specified for the current channel or for all channels on the
        connection. The particular properties and semantics of a qos method
        always depend on the content class semantics. Though the qos method
        could in principle apply to both peers, it is currently meaningful only
        for the server.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x003C000A
        name = 'Basic.Qos'

        # AMQP Method Attributes
        attributes = ["prefetch_size",
                      "prefetch_count",
                      "global_"]

        # Class Attribute Types
        prefetch_size = "long"
        prefetch_count = "short"
        global_ = "bit"

        def __init__(self, prefetch_size=0, prefetch_count=0, global_=False):
            """Initialize the Basic.Qos class

            :param prefetch_size: Prefetch window in octets
            :type prefetch_size: int/long
            :param prefetch_count: Prefetch window in messages
            :type prefetch_count: int
            :param global_: Apply to entire connection
            :type global_: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Basic.QosOk]

            # Prefetch window in octets
            self.prefetch_size = prefetch_size

            # Prefetch window in messages
            self.prefetch_count = prefetch_count

            # Apply to entire connection
            self.global_ = global_

    class QosOk(Frame):
        """Confirm the requested qos

        This method tells the client that the requested QoS levels could be
        handled by the server. The requested QoS applies to all active
        consumers until a new QoS is defined.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x003C000B
        name = 'Basic.QosOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Basic.QosOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Consume(Frame):
        """Start a queue consumer

        This method asks the server to start a "consumer", which is a transient
        request for messages from a specific queue. Consumers last as long as
        the channel they were declared on, or until the client cancels them.

        """
        # AMQP Method Number and Mapping Index
        id = 20
        index = 0x003C0014
        name = 'Basic.Consume'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "consumer_tag",
                      "no_local",
                      "no_ack",
                      "exclusive",
                      "nowait",
                      "arguments"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        consumer_tag = "shortstr"
        no_local = "bit"
        no_ack = "bit"
        exclusive = "bit"
        nowait = "bit"
        arguments = "table"

        def __init__(self, ticket=0, queue=None, consumer_tag=None,
                     no_local=False, no_ack=False, exclusive=False,
                     nowait=False, arguments={}):
            """Initialize the Basic.Consume class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param consumer_tag:
            :type consumer_tag: str
            :param no_local: Do not deliver own messages
            :type no_local: bool
            :param no_ack: No acknowledgement needed
            :type no_ack: bool
            :param exclusive: Request exclusive access
            :type exclusive: bool
            :param nowait: Do not send a reply method
            :type nowait: bool
            :param arguments: Arguments for declaration
            :type arguments: dict

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Basic.ConsumeOk]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            self.consumer_tag = consumer_tag

            # Do not deliver own messages
            self.no_local = no_local

            # No acknowledgement needed
            self.no_ack = no_ack

            # Request exclusive access
            self.exclusive = exclusive

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for declaration
            self.arguments = arguments

    class ConsumeOk(Frame):
        """Confirm a new consumer

        The server provides the client with a consumer tag, which is used by
        the client for methods called on the consumer at a later stage.

        """
        # AMQP Method Number and Mapping Index
        id = 21
        index = 0x003C0015
        name = 'Basic.ConsumeOk'

        # AMQP Method Attributes
        attributes = ["consumer_tag"]

        # Class Attribute Types
        consumer_tag = "shortstr"

        def __init__(self, consumer_tag=None):
            """Initialize the Basic.ConsumeOk class

            :param consumer_tag:
            :type consumer_tag: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            self.consumer_tag = consumer_tag

    class Cancel(Frame):
        """End a queue consumer

        This method cancels a consumer. This does not affect already delivered
        messages, but it does mean the server will not send any more messages
        for that consumer. The client may receive an arbitrary number of
        messages in between sending the cancel method and receiving the cancel-
        ok reply.  It may also be sent from the server to the client in the
        event of the consumer being unexpectedly cancelled (i.e. cancelled for
        any reason other than the server receiving the corresponding
        basic.cancel from the client). This allows clients to be notified of
        the loss of consumers due to events such as queue deletion. Note that
        as it is not a MUST for clients to accept this method from the client,
        it is advisable for the broker to be able to identify those clients
        that are capable of accepting the method, through some means of
        capability negotiation.

        """
        # AMQP Method Number and Mapping Index
        id = 30
        index = 0x003C001E
        name = 'Basic.Cancel'

        # AMQP Method Attributes
        attributes = ["consumer_tag",
                      "nowait"]

        # Class Attribute Types
        consumer_tag = "shortstr"
        nowait = "bit"

        def __init__(self, consumer_tag=None, nowait=False):
            """Initialize the Basic.Cancel class

            :param consumer_tag: Consumer tag
            :type consumer_tag: str
            :param nowait: Do not send a reply method
            :type nowait: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Basic.CancelOk]

            # Consumer tag
            self.consumer_tag = consumer_tag

            # Do not send a reply method
            self.nowait = nowait

    class CancelOk(Frame):
        """Confirm a cancelled consumer

        This method confirms that the cancellation was completed.

        """
        # AMQP Method Number and Mapping Index
        id = 31
        index = 0x003C001F
        name = 'Basic.CancelOk'

        # AMQP Method Attributes
        attributes = ["consumer_tag"]

        # Class Attribute Types
        consumer_tag = "shortstr"

        def __init__(self, consumer_tag=None):
            """Initialize the Basic.CancelOk class

            :param consumer_tag: Consumer tag
            :type consumer_tag: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Consumer tag
            self.consumer_tag = consumer_tag

    class Publish(Frame):
        """Publish a message

        This method publishes a message to a specific exchange. The message
        will be routed to queues as defined by the exchange configuration and
        distributed to any active consumers when the transaction, if any, is
        committed.

        """
        # AMQP Method Number and Mapping Index
        id = 40
        index = 0x003C0028
        name = 'Basic.Publish'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "exchange",
                      "routing_key",
                      "mandatory",
                      "immediate"]

        # Class Attribute Types
        ticket = "short"
        exchange = "shortstr"
        routing_key = "shortstr"
        mandatory = "bit"
        immediate = "bit"

        def __init__(self, ticket=0, exchange=None, routing_key=None,
                     mandatory=False, immediate=False):
            """Initialize the Basic.Publish class

            :param ticket: Deprecated
            :type ticket: int
            :param exchange:
            :type exchange: str
            :param routing_key: Message routing key
            :type routing_key: str
            :param mandatory: Indicate mandatory routing
            :type mandatory: bool
            :param immediate: Request immediate delivery
            :type immediate: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Deprecated
            self.ticket = ticket

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

            # Indicate mandatory routing
            self.mandatory = mandatory

            # Request immediate delivery
            self.immediate = immediate

    class Return(Frame):
        """Return a failed message

        This method returns an undeliverable message that was published with
        the "immediate" flag set, or an unroutable message published with the
        "mandatory" flag set. The reply code and text provide information about
        the reason that the message was undeliverable.

        """
        # AMQP Method Number and Mapping Index
        id = 50
        index = 0x003C0032
        name = 'Basic.Return'

        # AMQP Method Attributes
        attributes = ["reply_code",
                      "reply_text",
                      "exchange",
                      "routing_key"]

        # Class Attribute Types
        reply_code = "short"
        reply_text = "shortstr"
        exchange = "shortstr"
        routing_key = "shortstr"

        def __init__(self, reply_code=None, reply_text=None, exchange=None,
                     routing_key=None):
            """Initialize the Basic.Return class

            :param reply_code: Reply code from server
            :type reply_code: int
            :param reply_text: Localised reply text
            :type reply_text: str
            :param exchange:
            :type exchange: str
            :param routing_key: Message routing key
            :type routing_key: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Reply code from server
            self.reply_code = reply_code

            # Localised reply text
            self.reply_text = reply_text

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

    class Deliver(Frame):
        """Notify the client of a consumer message

        This method delivers a message to the client, via a consumer. In the
        asynchronous message delivery model, the client starts a consumer using
        the Consume method, then the server responds with Deliver methods as
        and when messages arrive for that consumer.

        """
        # AMQP Method Number and Mapping Index
        id = 60
        index = 0x003C003C
        name = 'Basic.Deliver'

        # AMQP Method Attributes
        attributes = ["consumer_tag",
                      "delivery_tag",
                      "redelivered",
                      "exchange",
                      "routing_key"]

        # Class Attribute Types
        consumer_tag = "shortstr"
        delivery_tag = "longlong"
        redelivered = "bit"
        exchange = "shortstr"
        routing_key = "shortstr"

        def __init__(self, consumer_tag=None, delivery_tag=None,
                     redelivered=False, exchange=None, routing_key=None):
            """Initialize the Basic.Deliver class

            :param consumer_tag: Consumer tag
            :type consumer_tag: str
            :param delivery_tag: Server-assigned delivery tag
            :type delivery_tag: int/long
            :param redelivered: Message is being redelivered
            :type redelivered: bool
            :param exchange:
            :type exchange: str
            :param routing_key: Message routing key
            :type routing_key: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Consumer tag
            self.consumer_tag = consumer_tag

            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Message is being redelivered
            self.redelivered = redelivered

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

    class Get(Frame):
        """Direct access to a queue

        This method provides a direct access to the messages in a queue using a
        synchronous dialogue that is designed for specific types of application
        where synchronous functionality is more important than performance.

        """
        # AMQP Method Number and Mapping Index
        id = 70
        index = 0x003C0046
        name = 'Basic.Get'

        # AMQP Method Attributes
        attributes = ["ticket",
                      "queue",
                      "no_ack"]

        # Class Attribute Types
        ticket = "short"
        queue = "shortstr"
        no_ack = "bit"

        def __init__(self, ticket=0, queue=None, no_ack=False):
            """Initialize the Basic.Get class

            :param ticket: Deprecated
            :type ticket: int
            :param queue:
            :type queue: str
            :param no_ack: No acknowledgement needed
            :type no_ack: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Basic.GetOk, Basic.GetEmpty]

            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # No acknowledgement needed
            self.no_ack = no_ack

    class GetOk(Frame):
        """Provide client with a message

        This method delivers a message to the client following a get method. A
        message delivered by 'get-ok' must be acknowledged unless the no-ack
        option was set in the get method.

        """
        # AMQP Method Number and Mapping Index
        id = 71
        index = 0x003C0047
        name = 'Basic.GetOk'

        # AMQP Method Attributes
        attributes = ["delivery_tag",
                      "redelivered",
                      "exchange",
                      "routing_key",
                      "message_count"]

        # Class Attribute Types
        delivery_tag = "longlong"
        redelivered = "bit"
        exchange = "shortstr"
        routing_key = "shortstr"
        message_count = "long"

        def __init__(self, delivery_tag=None, redelivered=False, exchange=None,
                     routing_key=None, message_count=None):
            """Initialize the Basic.GetOk class

            :param delivery_tag: Server-assigned delivery tag
            :type delivery_tag: int/long
            :param redelivered: Message is being redelivered
            :type redelivered: bool
            :param exchange:
            :type exchange: str
            :param routing_key: Message routing key
            :type routing_key: str
            :param message_count: Number of messages in queue
            :type message_count: int/long

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Message is being redelivered
            self.redelivered = redelivered

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

            # Number of messages in queue
            self.message_count = message_count

    class GetEmpty(Frame):
        """Indicate no messages available

        This method tells the client that the queue has no messages available
        for the client.

        """
        # AMQP Method Number and Mapping Index
        id = 72
        index = 0x003C0048
        name = 'Basic.GetEmpty'

        # AMQP Method Attributes
        attributes = ["cluster_id"]

        # Class Attribute Types
        cluster_id = "shortstr"

        def __init__(self, cluster_id=None):
            """Initialize the Basic.GetEmpty class

            :param cluster_id: Deprecated
            :type cluster_id: str

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Deprecated
            self.cluster_id = cluster_id

    class Ack(Frame):
        """Acknowledge one or more messages

        When sent by the client, this method acknowledges one or more messages
        delivered via the Deliver or Get-Ok methods.  When sent by server, this
        method acknowledges one or more messages published with the Publish
        method on a channel in confirm mode.  The acknowledgement can be for a
        single message or a set of messages up to and including a specific
        message.

        """
        # AMQP Method Number and Mapping Index
        id = 80
        index = 0x003C0050
        name = 'Basic.Ack'

        # AMQP Method Attributes
        attributes = ["delivery_tag",
                      "multiple"]

        # Class Attribute Types
        delivery_tag = "longlong"
        multiple = "bit"

        def __init__(self, delivery_tag=0, multiple=False):
            """Initialize the Basic.Ack class

            :param delivery_tag: Server-assigned delivery tag
            :type delivery_tag: int/long
            :param multiple: Acknowledge multiple messages
            :type multiple: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Acknowledge multiple messages
            self.multiple = multiple

    class Reject(Frame):
        """Reject an incoming message

        This method allows a client to reject a message. It can be used to
        interrupt and cancel large incoming messages, or return untreatable
        messages to their original queue.

        """
        # AMQP Method Number and Mapping Index
        id = 90
        index = 0x003C005A
        name = 'Basic.Reject'

        # AMQP Method Attributes
        attributes = ["delivery_tag",
                      "requeue"]

        # Class Attribute Types
        delivery_tag = "longlong"
        requeue = "bit"

        def __init__(self, delivery_tag=None, requeue=True):
            """Initialize the Basic.Reject class

            :param delivery_tag: Server-assigned delivery tag
            :type delivery_tag: int/long
            :param requeue: Requeue the message
            :type requeue: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Requeue the message
            self.requeue = requeue

    class RecoverAsync(Frame):
        """Redeliver unacknowledged messages

        This method asks the server to redeliver all unacknowledged messages on
        a specified channel. Zero or more messages may be redelivered.  This
        method is deprecated in favour of the synchronous Recover/Recover-Ok.

        """
        # AMQP Method Number and Mapping Index
        id = 100
        index = 0x003C0064
        name = 'Basic.RecoverAsync'

        # AMQP Method Attributes
        attributes = ["requeue"]

        # Class Attribute Types
        requeue = "bit"

        def __init__(self, requeue=False):
            """Initialize the Basic.RecoverAsync class

            :param requeue: Requeue the message
            :type requeue: bool

            :raises: DeprecationWarning

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Requeue the message
            self.requeue = requeue

            # This command is deprecated in AMQP 0-9-1
            raise DeprecationWarning(DEPRECATION_WARNING)

    class Recover(Frame):
        """Redeliver unacknowledged messages

        This method asks the server to redeliver all unacknowledged messages on
        a specified channel. Zero or more messages may be redelivered.  This
        method replaces the asynchronous Recover.

        """
        # AMQP Method Number and Mapping Index
        id = 110
        index = 0x003C006E
        name = 'Basic.Recover'

        # AMQP Method Attributes
        attributes = ["requeue"]

        # Class Attribute Types
        requeue = "bit"

        def __init__(self, requeue=False):
            """Initialize the Basic.Recover class

            :param requeue: Requeue the message
            :type requeue: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Requeue the message
            self.requeue = requeue

    class RecoverOk(Frame):
        """Confirm recovery

        This method acknowledges a Basic.Recover method.

        """
        # AMQP Method Number and Mapping Index
        id = 111
        index = 0x003C006F
        name = 'Basic.RecoverOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Basic.RecoverOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Nack(Frame):
        """Reject one or more incoming messages

        This method allows a client to reject one or more incoming messages. It
        can be used to interrupt and cancel large incoming messages, or return
        untreatable messages to their original queue.  This method is also used
        by the server to inform publishers on channels in confirm mode of
        unhandled messages.  If a publisher receives this method, it probably
        needs to republish the offending messages.

        """
        # AMQP Method Number and Mapping Index
        id = 120
        index = 0x003C0078
        name = 'Basic.Nack'

        # AMQP Method Attributes
        attributes = ["delivery_tag",
                      "multiple",
                      "requeue"]

        # Class Attribute Types
        delivery_tag = "longlong"
        multiple = "bit"
        requeue = "bit"

        def __init__(self, delivery_tag=0, multiple=False, requeue=True):
            """Initialize the Basic.Nack class

            :param delivery_tag: Server-assigned delivery tag
            :type delivery_tag: int/long
            :param multiple: Reject multiple messages
            :type multiple: bool
            :param requeue: Requeue the message
            :type requeue: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Reject multiple messages
            self.multiple = multiple

            # Requeue the message
            self.requeue = requeue

    class Properties(PropertiesBase):
        """Content Properties"""

        name = 'Basic.Properties'

        # Attributes
        attributes = ["content-type",
                      "content-encoding",
                      "headers",
                      "delivery-mode",
                      "priority",
                      "correlation-id",
                      "reply-to",
                      "expiration",
                      "message-id",
                      "timestamp",
                      "type",
                      "user-id",
                      "app-id",
                      "cluster-id"]

        # Flag Values
        flags = {"content-type": 32768,
                 "content-encoding": 16384,
                 "headers": 8192,
                 "delivery-mode": 4096,
                 "priority": 2048,
                 "correlation-id": 1024,
                 "reply-to": 512,
                 "expiration": 256,
                 "message-id": 128,
                 "timestamp": 64,
                 "type": 32,
                 "user-id": 16,
                 "app-id": 8,
                 "cluster-id": 4}

        # Class Attribute Types
        content_type = "shortstr"
        content_encoding = "shortstr"
        headers = "table"
        delivery_mode = "octet"
        priority = "octet"
        correlation_id = "shortstr"
        reply_to = "shortstr"
        expiration = "shortstr"
        message_id = "shortstr"
        timestamp = "timestamp"
        type = "shortstr"
        user_id = "shortstr"
        app_id = "shortstr"
        cluster_id = "shortstr"

        def __init__(self, content_type=None, content_encoding=None,
                     headers=None, delivery_mode=None, priority=None,
                     correlation_id=None, reply_to=None, expiration=None,
                     message_id=None, timestamp=None, type=None, user_id=None,
                     app_id=None, cluster_id=None):
            """Initialize the Basic.Properties class

            :param content_type: MIME content type
            :type content_type: str
            :param content_encoding: MIME content encoding
            :type content_encoding: str
            :param headers: Message header field table
            :type headers: dict
            :param delivery_mode: Non-persistent (1) or persistent (2)
            :type delivery_mode: int
            :param priority: Message priority, 0 to 9
            :type priority: int
            :param correlation_id: Application correlation identifier
            :type correlation_id: str
            :param reply_to: Address to reply to
            :type reply_to: str
            :param expiration: Message expiration specification
            :type expiration: str
            :param message_id: Application message identifier
            :type message_id: str
            :param timestamp: Message timestamp
            :type timestamp: struct_time
            :param type: Message type name
            :type type: str
            :param user_id: Creating user id
            :type user_id: str
            :param app_id: Creating application id
            :type app_id: str
            :param cluster_id: Deprecated
            :type cluster_id: str

            """

            # MIME content type
            self.content_type = content_type

            # MIME content encoding
            self.content_encoding = content_encoding

            # Message header field table
            self.headers = headers

            # Non-persistent (1) or persistent (2)
            self.delivery_mode = delivery_mode

            # Message priority, 0 to 9
            self.priority = priority

            # Application correlation identifier
            self.correlation_id = correlation_id

            # Address to reply to
            self.reply_to = reply_to

            # Message expiration specification
            self.expiration = expiration

            # Application message identifier
            self.message_id = message_id

            # Message timestamp
            self.timestamp = timestamp

            # Message type name
            self.type = type

            # Creating user id
            self.user_id = user_id

            # Creating application id
            self.app_id = app_id

            # Deprecated
            self.cluster_id = cluster_id


class Tx(object):
    """Work with transactions

    The Tx class allows publish and ack operations to be batched into atomic
    units of work.  The intention is that all publish and ack requests issued
    within a transaction will complete successfully or none of them will.
    Servers SHOULD implement atomic transactions at least where all publish or
    ack requests affect a single queue.  Transactions that cover multiple
    queues may be non-atomic, given that queues can be created and destroyed
    asynchronously, and such events do not form part of any transaction.
    Further, the behaviour of transactions with respect to the immediate and
    mandatory flags on Basic.Publish methods is not defined.

    """
    # AMQP Class Number and Mapping Index
    id = 90
    index = 0x005A0000

    class Select(Frame):
        """Select standard transaction mode

        This method sets the channel to use standard transactions. The client
        must use this method at least once on a channel before using the Commit
        or Rollback methods.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x005A000A
        name = 'Tx.Select'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Tx.Select class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Tx.SelectOk]

    class SelectOk(Frame):
        """Confirm transaction mode

        This method confirms to the client that the channel was successfully
        set to use standard transactions.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x005A000B
        name = 'Tx.SelectOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Tx.SelectOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Commit(Frame):
        """Commit the current transaction

        This method commits all message publications and acknowledgments
        performed in the current transaction.  A new transaction starts
        immediately after a commit.

        """
        # AMQP Method Number and Mapping Index
        id = 20
        index = 0x005A0014
        name = 'Tx.Commit'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Tx.Commit class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Tx.CommitOk]

    class CommitOk(Frame):
        """Confirm a successful commit

        This method confirms to the client that the commit succeeded. Note that
        if a commit fails, the server raises a channel exception.

        """
        # AMQP Method Number and Mapping Index
        id = 21
        index = 0x005A0015
        name = 'Tx.CommitOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Tx.CommitOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

    class Rollback(Frame):
        """Abandon the current transaction

        This method abandons all message publications and acknowledgments
        performed in the current transaction. A new transaction starts
        immediately after a rollback. Note that unacked messages will not be
        automatically redelivered by rollback; if that is required an explicit
        recover call should be issued.

        """
        # AMQP Method Number and Mapping Index
        id = 30
        index = 0x005A001E
        name = 'Tx.Rollback'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Tx.Rollback class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Tx.RollbackOk]

    class RollbackOk(Frame):
        """Confirm successful rollback

        This method confirms to the client that the rollback succeeded. Note
        that if an rollback fails, the server raises a channel exception.

        """
        # AMQP Method Number and Mapping Index
        id = 31
        index = 0x005A001F
        name = 'Tx.RollbackOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Tx.RollbackOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False


class Confirm(object):
    """Work with confirms

    The Confirm class allows publishers to put the channel in confirm mode and
    susequently be notified when messages have been handled by the broker.  The
    intention is that all messages published on a channel in confirm mode will
    be acknowledged at some point.  By acknowledging a message the broker
    assumes responsibility for it and indicates that it has done something it
    deems reasonable with it.  Unroutable mandatory or immediate messages are
    acknowledged right after the Basic.Return method. Messages are acknowledged
    when all queues to which the message has been routed have either delivered
    the message and received an acknowledgement (if required), or enqueued the
    message (and persisted it if required).  Published messages are assigned
    ascending sequence numbers, starting at 1 with the first Confirm.Select
    method. The server confirms messages by sending Basic.Ack methods referring
    to these sequence numbers.

    """
    # AMQP Class Number and Mapping Index
    id = 85
    index = 0x00550000

    class Select(Frame):
        """Select confirm mode (i.e. enable publisher acknowledgements)

        This method sets the channel to use publisher acknowledgements. The
        client can only use this method on a non-transactional channel.

        """
        # AMQP Method Number and Mapping Index
        id = 10
        index = 0x0055000A
        name = 'Confirm.Select'

        # AMQP Method Attributes
        attributes = ["nowait"]

        # Class Attribute Types
        nowait = "bit"

        def __init__(self, nowait=False):
            """Initialize the Confirm.Select class

            :param nowait: Do not send a reply method
            :type nowait: bool

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = True

            # Valid responses to this method
            self.valid_responses = [Confirm.SelectOk]

            # Do not send a reply method
            self.nowait = nowait

    class SelectOk(Frame):
        """Acknowledge confirm mode

        This method confirms to the client that the channel was successfully
        set to use publisher acknowledgements.

        """
        # AMQP Method Number and Mapping Index
        id = 11
        index = 0x0055000B
        name = 'Confirm.SelectOk'

        # AMQP Method Attributes
        attributes = []

        def __init__(self):
            """Initialize the Confirm.SelectOk class

            """
            # Specifies if this is a synchronous AMQP method
            self.synchronous = False

# AMQP Class.Method Index Mapping
INDEX_MAPPING = {0x000A000A: Connection.Start,
                 0x000A000B: Connection.StartOk,
                 0x000A0014: Connection.Secure,
                 0x000A0015: Connection.SecureOk,
                 0x000A001E: Connection.Tune,
                 0x000A001F: Connection.TuneOk,
                 0x000A0028: Connection.Open,
                 0x000A0029: Connection.OpenOk,
                 0x000A0032: Connection.Close,
                 0x000A0033: Connection.CloseOk,
                 0x0014000A: Channel.Open,
                 0x0014000B: Channel.OpenOk,
                 0x00140014: Channel.Flow,
                 0x00140015: Channel.FlowOk,
                 0x00140028: Channel.Close,
                 0x00140029: Channel.CloseOk,
                 0x0028000A: Exchange.Declare,
                 0x0028000B: Exchange.DeclareOk,
                 0x00280014: Exchange.Delete,
                 0x00280015: Exchange.DeleteOk,
                 0x0028001E: Exchange.Bind,
                 0x0028001F: Exchange.BindOk,
                 0x00280028: Exchange.Unbind,
                 0x00280033: Exchange.UnbindOk,
                 0x0032000A: Queue.Declare,
                 0x0032000B: Queue.DeclareOk,
                 0x00320014: Queue.Bind,
                 0x00320015: Queue.BindOk,
                 0x0032001E: Queue.Purge,
                 0x0032001F: Queue.PurgeOk,
                 0x00320028: Queue.Delete,
                 0x00320029: Queue.DeleteOk,
                 0x00320032: Queue.Unbind,
                 0x00320033: Queue.UnbindOk,
                 0x003C000A: Basic.Qos,
                 0x003C000B: Basic.QosOk,
                 0x003C0014: Basic.Consume,
                 0x003C0015: Basic.ConsumeOk,
                 0x003C001E: Basic.Cancel,
                 0x003C001F: Basic.CancelOk,
                 0x003C0028: Basic.Publish,
                 0x003C0032: Basic.Return,
                 0x003C003C: Basic.Deliver,
                 0x003C0046: Basic.Get,
                 0x003C0047: Basic.GetOk,
                 0x003C0048: Basic.GetEmpty,
                 0x003C0050: Basic.Ack,
                 0x003C005A: Basic.Reject,
                 0x003C0064: Basic.RecoverAsync,
                 0x003C006E: Basic.Recover,
                 0x003C006F: Basic.RecoverOk,
                 0x003C0078: Basic.Nack,
                 0x005A000A: Tx.Select,
                 0x005A000B: Tx.SelectOk,
                 0x005A0014: Tx.Commit,
                 0x005A0015: Tx.CommitOk,
                 0x005A001E: Tx.Rollback,
                 0x005A001F: Tx.RollbackOk,
                 0x0055000A: Confirm.Select,
                 0x0055000B: Confirm.SelectOk}
