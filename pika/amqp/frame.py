# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

"""
Manage the marshalling and demarshalling of AMQP frames

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-24'

import logging
import struct

from . import definitions
from . import header
from pika import codec


_FRAME_HEADER_SIZE = 7
_FRAME_END_SIZE = 1

_DEMARSHALLING_FAILURE = 0, 0, None
_LOGGER = logging.getLogger('pika.amqp.frame')


def demarshal(data_in):
    """Takes in binary data and maps builds the appropriate frame type,
    returning a frame object.

    :param data_in: Raw byte stream data
    :type data_in: unicode
    :returns: tuple of  bytes consumed, channel, and a frame object
    :raises: AMQPFrameError

    """
    # Look to see if it's a protocol header frame
    try:
        frame = _demarshal_protocol_header_frame(data_in)
        if frame:
            return 8, 0, frame
    except ValueError:
        _LOGGER.warning('Demarshalling error processing a ProtocolHeader '
                        'frame: %r', data_in)
        # It was a protocol header but it didn't decode properly
        return _DEMARSHALLING_FAILURE

    # split the data into parts
    frame_data = data_in.split(unichr(definitions.AMQP_FRAME_END))[0].encode('utf-8')

    # How much data we should consume
    bytes_consumed = len(frame_data)
    print repr(frame_data)

    # The lengths should not match, the frame end byte should be gone
    #if (bytes_consumed - 1) == len(data_in):
    #    return _DEMARSHALLING_FAILURE

    # Decode the low level frame and break it into parts
    try:
        frame_type, channel, frame_size = _frame_parts(frame_data)
        last_byte = _FRAME_HEADER_SIZE + frame_size + 1
        frame_data = frame_data[_FRAME_HEADER_SIZE:last_byte]
    except ValueError:
        _LOGGER.warning('Demarshalling error processing a content frame: %r',
                        data_in)
        return _DEMARSHALLING_FAILURE

    if frame_type == definitions.AMQP_FRAME_METHOD:
        return bytes_consumed, channel, _demarshal_method_frame(frame_data)

    elif frame_type == definitions.AMQP_FRAME_HEADER:
        return bytes_consumed, channel, _demarshal_header_frame(frame_data)

    #elif frame_type == amqp.AMQP_FRAME_BODY:
    #    consumed, frame_obj = decode_body_frame(channel, data, frame_end)

    #elif frame_type == amqp.AMQP_FRAME_HEARTBEAT:
    #    consumed, frame_obj = decode_heartbeat_frame(channel, data, frame_end)

    raise definitions.AMQPFrameError("Unknown frame type: %i" % frame_type)


def _demarshal_protocol_header_frame(data_in):
    """Attempt to demarshal a protocol header frame

    The ProtocolHeader is abbreviated in size and functionality compared to
    the rest of the frame types, so return _DEMARSHALLING_ERROR doesn't apply
    as cleanly since we don't have all of the attributes to return even
    regardless of success or failure.

    :param data_in: Raw byte stream data
    :type data_in: unicode
    :returns: header.ProtocolHeader
    :raises: ValueError

    """
    # Do the first four bytes not match?
    if data_in[0:4] != 'AMQP':
        return None

    try:
        frame = header.ProtocolHeader()
        frame.demarshal(data_in)
        return frame
    except IndexError:
        # We didn't get a full frame
        raise ValueError('Frame data did not meet minimum length requirements')


def _demarshal_method_frame(frame_data):
    """Attempt to demarshal a method frame

    :param frame_data: Raw frame data to assign to our method frame
    :type frame_data: unicode
    :returns: tuple of the amount of data consumed and the frame object

    """
    # Get the Method Index from the class data
    bytes_used, method_index = codec.decode.long_int(frame_data)

    # Create an instance of the method object we're going to demarshal
    method = definitions.INDEX_MAPPING[method_index]()

    # Demarshal the data
    method.demarshal(frame_data[bytes_used:])

    #  Demarshal the data in the object and return it
    return method


def _demarshal_header_frame(frame_data):
    """Attempt to demarshal a header frame

    :param frame_data: Raw frame data to assign to our header frame
    :type frame_data: unicode
    :returns: tuple of the amount of data consumed and the frame object

    """
    content_header = header.ContentHeader()
    content_header.demarshal(frame_data)
    return content_header


def _frame_parts(data_in):
    """Try and decode a low-level AMQP frame and return the parts of the frame.

    :param data_in: Raw byte stream data
    :type data_in: unicode
    :returns: tuple of frame type, channel number, and frame data to decode
    :raises: ValueError
    :raises: AMQPFrameError

    """
    # Get the Frame Type, Channel Number and Frame Size
    try:
        return struct.unpack('>BHL', data_in[0:_FRAME_HEADER_SIZE])
    except struct.error:
        # We didn't get a full frame
        return _DEMARSHALLING_FAILURE

