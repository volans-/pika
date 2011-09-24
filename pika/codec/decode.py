# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""
AMQP Data Decoder

Functions for decoding data of various types including field tables and arrays

"""
__author__ = 'Gavin M. Roy <gmr@myyearbook.com>'
__since__ = '2011-03-30'

import decimal as _decimal
import struct
import time


def boolean(value):
    """Decode a boolean value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a bool value.

    """

    return 1, bool(struct.unpack_from('>B', value)[0])


def decimal(value):
    """Decode a decimal value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a decimal.Decimal value.

    """
    decimals = struct.unpack_from('>B', value)[0]
    raw = struct.unpack_from('>i', value, 1)[0]
    return 5, _decimal.Decimal(raw) * (_decimal.Decimal(10) ** -decimals)


def floating_point(value):
    """Decode a floating point value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a float value.

    """
    return 4, struct.unpack_from('>f', value)[0]


def long_int(value):
    """Decode a long integer value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and an int value.

    """
    return 4, struct.unpack_from('>l', value)[0]


def long_long_int(value):
    """Decode a long-long integer value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and an int value.

    """
    return 8, struct.unpack_from('>q', value)[0]


def short_int(value):
    """Decode a short integer value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and an int value.

    """
    return 2, struct.unpack_from('>h', value)[0]


def short_string(value):
    """Decode a string value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a str value.

    """
    length = struct.unpack_from('>B', value)[0]
    return length + 1, value[1:length + 1]


def long_string(value):
    """Decode a string value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a str value.

    """
    length = struct.unpack_from('>I', value)[0]
    return length + 4, value[4:length + 4]


def timestamp(value):
    """Decode a timestamp value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a struct_time value

    """
    return 8, time.gmtime(struct.unpack_from('>Q', value)[0])


def field_array(value):
    """Decode a field array value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a list.

    """
    length = struct.unpack_from('>l', value)[0]
    offset = 4
    data = list()
    field_array_end = offset + length
    while offset < field_array_end:
        consumed, result = _decode_value(value[offset:])
        offset += consumed
        data.append(result)
    return field_array_end, data


def field_table(value):
    """Decode a field array value.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes used and a dict.

    """
    length = struct.unpack_from('>l', value)[0]
    offset = 4
    data = dict()
    field_table_end = offset + length
    while offset < field_table_end:
        keysize = struct.unpack_from('B', value, offset)[0] + 1
        key = value[offset + 1:offset + keysize]
        offset += keysize
        consumed, result = _decode_value(value[offset:])
        offset += consumed
        data[key] = result
    return field_table_end, data


def _decode_value(value):
    """Takes in a value looking at the first byte to determine which decoder to
    use.

    :param value: Value to decode.
    :type value: str.
    :returns: tuple of bytes consumed and mixed.

    """
    # Determine the field type and encode it
    if value[0] == 'A':
        consumed, result = field_array(value[1:])
    elif value[0] == 'D':
        consumed, result = decimal(value[1:])
    elif value[0] == 'f':
        consumed, result = floating_point(value[1:])
    elif value[0] == 'F':
        consumed, result = field_table(value[1:])
    elif value[0] == 'I':
        consumed, result = long_int(value[1:])
    elif value[0] == 'L':
        consumed, result = long_long_int(value[1:])
    elif value[0] == 't':
        consumed, result = boolean(value[1:])
    elif value[0] == 'T':
        consumed, result = timestamp(value[1:])
    elif value[0] == 's':
        consumed, result = short_string(value[1:])
    elif value[0] == 'S':
        consumed, result = long_string(value[1:])
    elif value[0] == 'U':
        consumed, result = short_int(value[1:])
    elif value[0] == '\x00':
        consumed, result = 0, None
    else:
        raise ValueError("Unknown type: %s", value[0])
    # Return the bytes used and the decoded value
    return consumed + 1, result


def decode_by_type(value, data_type):
    """Decodes values using the specified type.

    :param value: Value to decode.
    :type value: str.
    :param data_type: type of data to decode.
    :type data_type: str.
    :returns: tuple of bytes used, mixed based on field type

    """
    # Determine the field type and encode it
    if data_type == 'bit':
        consumed, result = boolean(value)
    elif data_type == 'long':
        consumed, result = long_int(value)
    elif data_type == 'longlong':
        consumed, result = long_long_int(value)
    elif data_type == 'longstr':
        consumed, result = long_string(value)
    elif data_type == 'short':
        consumed, result = short_int(value)
    elif data_type == 'shortstr':
        consumed, result = short_string(value)
    elif data_type == 'table':
        consumed, result = field_table(value)
    elif data_type == 'timestamp':
        consumed, result = timestamp(value)
    else:
        raise ValueError("Unknown type: %s", value)
    # Return the bytes used and the decoded value
    return consumed, result


# Define a data type mapping to methods
METHODS = {"bit": boolean,
           "long": long_int,
           "longlong": long_long_int ,
           "longstr": long_string,
           "short": short_int,
           "shortstr": short_string,
           "table": field_table,
           "timestamp": timestamp}
