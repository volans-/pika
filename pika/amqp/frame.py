# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

"""
frame.py

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-24'

import logging
import struct

from . import definitions
from . import header
from pika import codec


_CONTENT_FRAME_HEADER_SIZE = 7
_CONTENT_FRAME_END_SIZE = 1
_CONTENT_FRAME_END_BYTE = 206
_DEMARSHALLING_FAILURE = 0, None, None, None
_LOGGER = logging.getLogger('pika.amqp.frame')


def demarshal(data_in):
    """Takes in binary data and maps builds the appropriate frame type,
    returning a frame object.

    :param data_in: Raw byte stream data.
    :type data_in: unicode.
    :returns: tuple of bytes consumed and obj.
    :raises: AMQPFrameError.

    """
    # Look to see if it's a protocol header frame
    try:
        consumed, frame = _demarshal_protocol_header_frame(data_in)
        if consumed:
            return consumed, frame
    except ValueError:
        _LOGGER.warning('Could not demarshal the expected ProtocolHeader frame')
        # It was a protocol header but it didn't decode properly
        return _DEMARSHALLING_FAILURE

    # Decode the low level frame and break it into parts
    try:
        frame_type, channel, frame_end, data = _frame_parts(data_in)
    except ValueError:
        return _DEMARSHALLING_FAILURE

    if frame_type == definitions.AMQP_FRAME_METHOD:
        return channel, _demarshal_method_frame(data, frame_end)

    #elif frame_type == amqp.AMQP_FRAME_HEADER:
    #    return decode_header_frame(channel, data, frame_end)

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
    :returns: tuple of bytes consumed and frame object
    :raises: ValueError

    """
    # Do the first four bytes not match?
    if data_in[0:4] != 'AMQP':
        return 0, None

    try:
        frame = header.ProtocolHeader()
        bytes_consumed = frame.demarshal(data_in)
        return bytes_consumed, frame
    except IndexError:
        # We didn't get a full frame
        raise ValueError('Frame data did not meet minimum length requirements')


def _demarshal_method_frame(frame_data, frame_end):
    """Attempt to demarshal a method frame

    :param frame_data: Raw frame data to assign to our method frame
    :type frame_data: unicode
    :param frame_end: Offset where the frame is supposed to end
    :type frame_end: int
    :returns: tuple of the amount of data consumed and the frame object

    """
    # Get the Method Index from the class data
    bytes_used, method_index = codec.decode.long_int(frame_data)

    # Create an instance of the method object we're going to demarshal
    method = definitions.INDEX_MAPPING[method_index]()

    # Demarshal the data in the object
    consumed = method.demarshal(frame_data[1:frame_end]) + 1

    # Return the bytes consumed and the method object
    return consumed, method


def _frame_parts(data_in):
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
                                     data_in[0:_CONTENT_FRAME_HEADER_SIZE])
    except struct.error:
        # We didn't get a full frame
        return _DEMARSHALLING_FAILURE

    # Get the frame data size
    frame_end = data_in.find(chr(definitions.AMQP_FRAME_END))

    # Validate the frame size vs the frame end position

    # We don't have all of the frame yet
    if frame_end > len(data_in):
        raise ValueError

    # The Frame termination chr is wrong
    if data_in[frame_end] != chr(_CONTENT_FRAME_END_BYTE):
        raise definitions.AMQPFrameError("Invalid CONTENT_FRAME_END_BYTE")

    # Return the values, including the raw frame data
    return (frame_type,
            channel_number,
            frame_end,
            data_in[_CONTENT_FRAME_HEADER_SIZE:frame_end])

