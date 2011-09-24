# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""AMQP Data Encoder

Functions for encoding data of various types including field tables and arrays

"""
__author__ = 'Gavin M. Roy <gmr@myyearbook.com>'
__since__ = '2011-03-29'

import calendar
import decimal as _decimal
import datetime
import struct
import time


def boolean(value):
    """Encode a boolean value.

    :param value: Value to encode.
    :type value: boolean.
    :returns: str.

    """
    if not isinstance(value, bool):
        raise ValueError("bool type required")
    return struct.pack('>cB', 't', int(value))


def decimal(value):
    """Encode a decimal.Decimal value.

    :param value: Value to encode.
    :type value: decimal.Decimal.
    :returns: str.

    """
    if not isinstance(value, _decimal.Decimal):
        raise ValueError("decimal.Decimal type required")
    value = value.normalize()
    if value._exp < 0:
        decimals = -value._exp
        raw = int(value * (_decimal.Decimal(10) ** decimals))
        return struct.pack('>cBi', 'D', decimals, raw)
    # per spec, the "decimal.Decimals" octet is unsigned (!)
    return struct.pack('>cBi', 'D', 0, int(value))


def floating_point(value):
    """Encode a floating point value.

    :param value: Value to encode.
    :type value: float.
    :returns: str.

    """
    if not isinstance(value, float):
        raise ValueError("float type required")
    return struct.pack('>cf', 'f',  value)


def long_int(value):
    """Encode a long integer.

    :param value: Value to encode.
    :type value: long, int.
    :returns: str.

    """
    if not isinstance(value, long) and not isinstance(value, int):
        raise ValueError("int or long type required")
    if value < -2147483648 or value > 2147483647:
        raise ValueError("Long integer range: -2147483648 to 2147483647")
    return struct.pack('>cl', 'I', value)


def long_long_int(value):
    """Encode a long-long int.

    :param value: Value to encode.
    :type value: long, int.
    :returns: str.

    """
    if not isinstance(value, long) and not isinstance(value, int):
        raise ValueError("int or long type required")
    if value < -9223372036854775808 or value > 9223372036854775807:
        raise ValueError("long-long integer range: \
-9223372036854775808 to 9223372036854775807")
    return struct.pack('>cq', 'L', value)


def long_string(value):
    """Encode a string.

    :param value: Value to encode.
    :type value: str.
    :returns: str.

    """
    if not isinstance(value, basestring):
        raise ValueError("str or unicode type required")
    return struct.pack('>cI', 'S', len(value)) + value


def short_int(value):
    """Encode a short integer.

    :param value: Value to encode.
    :type value: int.
    :returns: str.

    """
    if not isinstance(value, int):
        raise ValueError("int type required")
    if value < -32768 or value > 32767:
        raise ValueError("Short range: -32768 to 32767")
    return struct.pack('>ch', 'U', value)


def short_string(value):
    """ Encode a string.

    :param value: Value to encode.
    :type value: str.
    :returns: str.

    """
    if not isinstance(value, basestring):
        raise ValueError("str or unicode type required")
    return struct.pack('>cB', 's', len(value)) + value


def timestamp(value):
    """Encode a datetime.datetime object or time.struct_time.

    :param value: Value to encode.
    :type value: datetime.datetime or time.struct_time value.
    :returns: str.

    """
    if isinstance(value, datetime.datetime):
        value = value.timetuple()
    if isinstance(value, time.struct_time):
        return struct.pack('>cQ', 'T', calendar.timegm(value))
    raise ValueError("datetime.datetime or time.struct_time type required")


def field_array(value):
    """Encode a field array from a dictionary.

    :param value: Value to encode.
    :type value: list.
    :returns: str.

    """
    if not isinstance(value, list):
        raise ValueError("list type required")

    data = list()
    for item in value:
        data.append(_encode_value(item))

    output = ''.join(data)
    return struct.pack('>cI', 'A', len(output)) + output


def field_table(value):
    """Encode a field table from a dictionary.

    :param value: Value to encode.
    :type value: dict.
    :returns: str.

    """
    # If there is no value, return a standard 4 null bytes
    if not value:
        return struct.pack('>I', 0)

    if not isinstance(value, dict):
        raise ValueError("dict type required, got %s", type(value))

    # Iterate through all of the keys and encode the data into a table
    data = list()
    for key in value:
        # Append the field header / delimiter
        data.append(struct.pack('B', len(key)))
        data.append(key)
        try:
            data.append(_encode_value(value[key]))
        except ValueError as err:
            raise ValueError("%s error: %s", key, err)

    # Join all of the data together as a string
    output = ''.join(data)
    return struct.pack('>cI', 'F', len(output)) + output


def _encode_integer(value):
    """Determines the best type of numeric type to encode value as, preferring
    the smallest data size first.

    :param value: Value to encode.
    :type value: int, long.
    :returns: str.

    """
    # Send the appropriately sized data value
    if -32768 < value < 32767:
        result = short_int(int(value))
    elif -2147483648 < value < 2147483647:
        result = long_int(long(value))
    elif -9223372036854775808 < value < 9223372036854775807:
        result = long_long_int(long(value))
    else:
        raise ValueError("Numeric value exceeds long-long-int max: %r",
                         value)

    # Return the encoded value
    return result


def _encode_value(value):
    """Takes a value of any type and tries to encode it with the proper encoder.

    :param value: Value to encode.
    :type value: mixed.
    :returns: str.

    """
    # Determine the field type and encode it
    if isinstance(value, bool):
        result = boolean(value)
    elif isinstance(value, int) or isinstance(value, long):
        result = _encode_integer(value)
    elif isinstance(value, _decimal.Decimal):
        result = decimal(value)
    elif isinstance(value, float):
        result = floating_point(value)
    elif isinstance(value, basestring):
        if len(value) < 255:
            result = short_string(value)
        else:
            result = long_string(value)
    elif isinstance(value, datetime.datetime) or isinstance(value,
                                                            time.struct_time):
        result = timestamp(value)
    elif isinstance(value, dict):
        result = field_table(value)
    elif isinstance(value, list):
        result = field_array(value)
    else:
        raise ValueError("Unknown type: %s (%r)", type(value), value)

    # Return the encoded value
    return result
