# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-04-10'

from amqp import definitions as amqp
import codec
import struct

CONTENT_FRAME_HEADER_SIZE = 7
CONTENT_FRAME_END_SIZE = 1
CONTENT_FRAME_END_BYTE = 206

DECODING_FAILURE = 0, None, None, None


def decode_protocol_header_frame(data_in):
    """Attempt to decode a protocol header frame

    :param data_in: Raw byte stream data.
    :type data_in: unicode.
    :returns: tuple of bytes consumed and obj.
    :raises: ValueError.

    """
    try:
        if data_in[0:4] == 'AMQP':
            major, minor, revision = struct.unpack_from('BBB', data_in, 5)
            return 8, ProtocolHeader(major, minor, revision)
    except IndexError:
        # We didn't get a full frame
        raise ValueError
    except struct.error:
        # We didn't get a full frame
        raise ValueError

    return DECODING_FAILURE


def decode_frame_parts(data_in):
    """Try and decode a low-level AMQP frame and return the parts of the frame.

    :param data_in: Raw byte stream data.
    :type data_in: unicode.
    :returns: tuple of frame type, channel number, frame_end offset and
              the frame data to decode.
    :raises: ValueError.
    :raises: AMQPFrameError.

    """
    # Get the Frame Type, Channel Number and Frame Size
    try:
        (frame_type,
         channel_number,
         frame_size) = struct.unpack('>BHL',
                                     data_in[0:CONTENT_FRAME_HEADER_SIZE])
    except struct.error:
        # We didn't get a full frame
        return DECODING_FAILURE

    # Get the frame data size
    frame_end = data_in.find(chr(amqp.AMQP_FRAME_END))

    # Validate the frame size vs the frame end position

    # We don't have all of the frame yet
    if frame_end > len(data_in):
        raise ValueError

    # The Frame termination chr is wrong
    if data_in[frame_end] != chr(CONTENT_FRAME_END_BYTE):
        raise amqp.AMQPFrameError("Invalid CONTENT_FRAME_END_BYTE marker")

    # Return the values, including the raw frame data
    return (frame_type,
            channel_number,
            frame_end,
            data_in[CONTENT_FRAME_HEADER_SIZE:frame_end])


def decode_method_frame(channel_number, frame_data, frame_end):
    """Attempt to decode a method frame.

    :param channel_number: Channel number the frame is for.
    :type channel_number: int.
    :param frame_data: Raw frame data to assign to our method frame.
    :type frame_data: unicode.
    :param frame_end: Offset where the frame is supposed to end.
    :type frame_end: int.
    :returns: tuple of the amount of data consumed and the frame object.

    """
    # Get the Method Index from the class data
    bytes_used, method_index = codec.decode.long_int(frame_data)
    offset = bytes_used

    # Return the amount of data consumed and the Method object
    return frame_end + 1, MethodFrame(channel_number,
                                      method_index,
                                      frame_data[offset:])


def decode_header_frame(frame_data, channel_number, frame_end):
    """Attempt to decode a method frame.

    :param channel_number: Channel number the frame is for.
    :type channel_number: int.
    :param frame_data: Raw frame data to assign to our method frame.
    :type frame_data: unicode.
    :returns: tuple of the amount of data consumed and the frame object.
    :param frame_end: Offset where the frame is supposed to end.
    :type frame_end: int.
    :returns: tuple of the amount of data consumed and the frame object.

    """
    # Return the header class and body size
    class_id, weight, body_size = struct.unpack_from('>HHQ', frame_data)

    """
    # Get the Properties type
    properties = amqp.props[class_id]()

    print repr(properties)

    # Decode the properties
    out = properties.decode(frame_data[12:])

    print repr(properties)

    # Return a Header frame
    return frame_end, HeaderFrame(channel_number, body_size, properties)
    """
    pass


def decode_body_frame(frame_data, channel_number, frame_end):
    """

        # Return the amount of data consumed and the Body frame w/ data
        return frame_end, Body(channel_number, frame_data)

    """
    pass


def decode_heartbeat_frame(frame_data, channel_number, frame_end):
    """
    """
    pass



def decode_frame(data_in):
    """Takes in binary data and maps builds the appropriate frame type,
    returning a frame object.

    :param data_in: Raw byte stream data.
    :type data_in: unicode.
    :returns: tuple of bytes consumed and obj.
    :raises: AMQPFrameError.

    """
    # Look to see if it's a protocol header frame
    try:
        value = decode_protocol_header_frame(data_in)
        if value[0]:
            return value
    except ValueError:
        # It was a protocol header but it didn't decode properly
        return DECODING_FAILURE

    # Decode the low level frame and break it into parts
    try:
        frame_type, channel, frame_end, data = decode_frame_parts(data_in)
    except ValueError:
        return DECODING_FAILURE

    if frame_type == amqp.AMQP_FRAME_METHOD:
        consumed, frame_obj = decode_method_frame(channel, data, frame_end)
    elif frame_type == amqp.AMQP_FRAME_HEADER:
        consumed, frame_obj = decode_header_frame(channel, data, frame_end)
    elif frame_type == amqp.AMQP_FRAME_BODY:
        consumed, frame_obj = decode_body_frame(channel, data, frame_end)
    elif frame_type == amqp.AMQP_FRAME_HEARTBEAT:
        consumed, frame_obj = decode_heartbeat_frame(channel, data, frame_end)
    else:
        raise amqp.AMQPFrameError("Unknown frame type: %i" % frame_type)

    # Return the bytes_consumed and frame obj
    return consumed, frame_obj


class ProtocolHeader(object):
    """Class that represents the AMQP Protocol Header"""

    def __init__(self, major_version=None, minor_version=None, revision=None):
        """Construct a Protocol Header frame object for the specified AMQP
        version.

        :param major_version: Major version number.
        :type major_version: int.
        :param minor_version: Minor version number.
        :type minor_version: int.
        :param revision: Revision number.
        :type revision: int.
        """
        self.major_version = major_version or amqp.AMQP_VERSION[0]
        self.minor_version = minor_version or amqp.AMQP_VERSION[1]
        self.revision = revision or amqp.AMQP_VERSION[2]

    def encode(self):
        """Return the full AMQP wire protocol frame data representation of the
        ProtocolHeader frame.

        :returns: unicode.
        """
        return u'AMQP' + struct.pack('BBBB', 0,
                                     self.major_version,
                                     self.minor_version,
                                     self.revision)


class MethodFrame(object):

    def __init__(self, channel, method_index, data_in=None):
        """Represents an AMQP Method Frame.

        :param channel: Channel Number.
        :type channel: int.
        :param method_index: The index mapping # for the AMQP Method/Class.
        :type method_index: int.
        :param data_in: Data that represents values assigned to this frame.
        :type data_in: str.

        """
        self.channel = channel
        self.method_class = amqp.INDEX_MAPPING[method_index]
        self.frame = self.method_class()

class HeaderFrame(object):
    pass
