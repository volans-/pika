# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-03-29'

import test_support
import pika.codec as codec

from datetime import datetime
import decimal
import time

# -- Helpers --

# -- Decoding Tests --


def test_decode_none():
    length, expectation = codec.decode._embedded_value('\x00')
    if expectation is not None:
        assert False, \
            "decode._embedded_value did not return None: %r" % expectation


def test_decode_unknown():
    try:
        codec.decode._embedded_value('Z\x00')
    except ValueError:
        return
    assert False, "decode._embedded_value did not raise a ValueError Exception"


def test_by_type_unknown():
    try:
        codec.decode.by_type('Z\x00', 'foobar')
    except ValueError:
        return
    assert False, "decode.by_type did not raise a ValueError Exception"


def test_decode_bool_false():
    value = '\x00'
    length, expectation = codec.decode.boolean(value)
    if not isinstance(expectation, bool):
        assert False, "decode.boolean did not return a bool: %r" % expectation
    if expectation:
        assert False, "decode.boolean did not return False: %r" % expectation


def test_decode_bool_true():
    value = '\x01'
    length, expectation = codec.decode.boolean(value)
    if not isinstance(expectation, bool):
        assert False, "decode.boolean did not return a bool: %r" % expectation
    if not expectation:
        assert False, "decode.boolean did not return True: %r" % expectation


def test_decode_decimal():
    value = '\x05\x00\x04\xcb/'
    length, expectation = codec.decode.decimal(value)
    if not isinstance(expectation, decimal.Decimal):
        assert False, "decode.decimal did not return a Decimal: %r" % \
                      expectation
    if expectation != decimal.Decimal('3.14159'):
        assert False, "decode.decimal did not return 3.14159: %r" % expectation


def test_decode_float():
    value = '@I\x0f\xd0'
    length, expectation = codec.decode.floating_point(value)
    if not isinstance(expectation, float):
        assert False, "decode.floating_point did not return a float: %r" % \
                      expectation
    if round(expectation, 5) != 3.14159:
        assert False, "decode.floating_point did not return 3.14159: %r" % \
                      round(expectation, 5)


def test_decode_long():
    value = '\x7f\xff\xff\xff'
    length, expectation = codec.decode.long_int(value)
    if not isinstance(expectation, int) and not isinstance(expectation, long):
        assert False, "decode.long_int did not return an int: %r" % expectation
    if expectation != 2147483647:
        assert False, "decode.long_int did not return 2147483647: %r" % \
                      expectation


def test_by_type_long():
    value = '\x7f\xff\xff\xff\xff\xff\xff\xf8'
    length, expectation = codec.decode.by_type(value, 'longlong')
    if not isinstance(expectation, int) and not isinstance(expectation, long):
        assert False, "decode.by_type did not return an int: %r" % expectation
    if expectation != long(9223372036854775800):
        assert False, \
            "decode.by_type did not return 9223372036854775800: %r" % \
            expectation


def test_decode_long_long():
    value = '\x7f\xff\xff\xff\xff\xff\xff\xf8'
    length, expectation = codec.decode.long_long_int(value)
    if not isinstance(expectation, int) and not isinstance(expectation, long):
        assert False, "decode.long_int did not return an int: %r" % expectation
    if expectation != 9223372036854775800:
        assert False, \
        "decode.long_long_int did not return 9223372036854775800: %r" % expectation


def test_decode_short():
    value = '\x7f\xff'
    length, expectation = codec.decode.short_int(value)
    if not isinstance(expectation, int):
        assert False, "decode.short_int did not return an int: %r" % expectation
    if expectation != 32767:
        assert False, "decode.short_int did not return 32767: %r" % expectation


def test_decode_long_string():
    value = '\x00\x00\x00\n0123456789'
    length, expectation = codec.decode.long_string(value)
    if not isinstance(expectation, basestring):
        assert False, "decode.long_string did not return a str: %r" % expectation
    if expectation != '0123456789':
        assert False, \
            "decode.long_string did not return '0123456789': %r" % expectation


def test_by_type_long_string():
    value = '\x00\x00\x00\n0123456789'
    length, expectation = codec.decode.by_type(value, 'longstr')
    if not isinstance(expectation, basestring):
        assert False, "decode.by_type did not return a str: %r" % expectation
    if expectation != '0123456789':
        assert False, \
            "decode.by_type did not return '0123456789': %r" % expectation


def test_table_value_short_string():
    value = 's\n0123456789'
    length, expectation = codec.decode._embedded_value(value)
    if not isinstance(expectation, basestring):
        assert False, "decode._embedded_value did not return a str: %r" % expectation
    if expectation != '0123456789':
        assert False, \
            "decode._embedded_value did not return '0123456789': %r" % expectation


def test_decode_short_string():
    value = '\n0123456789'
    length, expectation = codec.decode.short_string(value)
    if not isinstance(expectation, basestring):
        assert False, "decode.short_string did not return a str: %r" % expectation
    if expectation != '0123456789':
        assert False, \
            "decode.short_string did not return '0123456789': %r" % expectation


def test_table_value_short_string():
    value = 's\n0123456789'
    length, expectation = codec.decode._embedded_value(value)
    if not isinstance(expectation, basestring):
        assert False, \
            "decode._embedded_value did not return a str: %r" % expectation
    if expectation != '0123456789':
        assert False, \
            ("decode._embedded_value return value did not match "
             "the expectation: %r" % expectation)


def test_table_value_x00():
    value = '\x00'
    length, expectation = codec.decode._embedded_value(value)
    if length != 0 and expectation is not None:
        assert False, \
            'decode._embedded_value for \x00 did not return 0, None: %r' % \
            expectation


def test_table_value_unknown():
    value = 'GOOD'
    try:
        length, expectation = codec.decode._embedded_value(value)
    except ValueError:
        return

    assert False, \
        'decode._embedded_value did not throw a ValueError: %r' % expectation


def test_decode_timestamp():
    value = '\x00\x00\x00\x00Ec)\x92'
    length, expectation = codec.decode.timestamp(value)
    if not isinstance(expectation, time.struct_time):
        assert False, "decode.timestamp did not return a struct_time: %r" % \
                      expectation
    if time.mktime(expectation) != \
       time.mktime((2006, 11, 21, 16, 30, 10, 1, 325, 0)):
        assert False, \
        "decode.timestamp did not return '2006, 11, 21, 16, 30, 10': %r" % \
        expectation


def test_by_type_timestamp():
    value = '\x00\x00\x00\x00Ec)\x92'
    length, expectation = codec.decode.by_type(value, 'timestamp')
    if not isinstance(expectation, time.struct_time):
        assert False, \
            "decode.by_type did not return a struct_time: %r" % expectation
    if time.mktime(expectation) != \
       time.mktime((2006, 11, 21, 16, 30, 10, 1, 325, 0)):
        assert False, ("decode.by_type did not return '2006, "
                       "11, 21, 16, 30, 10': %r" % expectation)


def test_decode_field_array():
    value = '\x00\x00\x00<U\x00\x01I\x00\x00\xaf\xc8S\x00\x00\x00\x04TestT\
\x00\x00\x00\x00Ec)\x92I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H\xf5\xc3L\x00\x00\
\x00\x00\xc4e5\xffL\x80\x00\x00\x00\x00\x00\x00\x08'
    data = [1, 45000, 'Test',  datetime(2006, 11, 21, 16, 30, 10).timetuple(),
            -1147483648, decimal.Decimal('3.14'), 3.14, long(3294967295),
            -9223372036854775800]
    length, expectation = codec.decode.field_array(value)
    if not isinstance(expectation, list):
        assert False, \
            "decode.field_array did not return a list: %r" % expectation
    test_support.compare_lists(data, expectation, 'decode.field_array')


def test_decode_field_table():
    value = '\x00\x00\x00\x92\x07longvalI6e&U\x08floatvlaf@H\xf5\xc3\x07\
boolvalt\x01\x06strvalS\x00\x00\x00\x04Test\x06intvalU\x00\x01\x0ctimestampval\
T\x00\x00\x00\x00Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08arrayvalA\x00\x00\x00\
\tU\x00\x01U\x00\x02U\x00\x03\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00\x00\
\x03bar'
    data = {'intval': 1,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime(2006, 11, 21, 16, 30, 10).timetuple(),
            'decval': decimal.Decimal('3.14'),
            'floatvla': 3.14,
            'longval': long(912598613),
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3]}
    length, expectation = codec.decode.field_table(value)
    if not isinstance(expectation, dict):
        assert False, \
            "decode.field_table did not return a dict: %r" % expectation
    test_support.compare_dicts(data, expectation, 'decode.field_table')


def test_decode_by_value_long_string():
    expected_response = ''.join([' ' for position in xrange(0, 1024)])
    value = '\x00\x00\x04\x00' + expected_response
    consumed, response = codec.decode.by_type(value, 'longstr')
    if response != expected_response:
        assert False, \
            "decode.by_type did not return the expected value: %r" % \
            response


def test_decode_by_value_table():
    data = ('\x00\x00\x04\r\x07longvalI6e&U\x08floatvalf@H\xf5\xc3\x07'
            'boolvalt\x01\x06strvals\x04Test\x06intvalU\x00\x01\x07longstr'
            'S\x00\x00\x03t00000000000000000000000000000000000000000000000'
            '0000011111111111111111111111111111111111111111111111111112222'
            '2222222222222222222222222222222222222222222222221111111111111'
            '1111111111111111111111111111111111111112222222222222222222222'
            '2222222222222222222222222222221111111111111111111111111111111'
            '1111111111111111111112222222222222222222222222222222222222222'
            '2222222222221111111111111111111111111111111111111111111111111'
            '1112222222222222222222222222222222222222222222222222222111111'
            '1111111111111111111111111111111111111111111111222222222222222'
            '2222222222222222222222222222222222222111111111111111111111111'
            '1111111111111111111111111111222222222222222222222222222222222'
            '2222222222222222222111111111111111111111111111111111111111111'
            '1111111111222222222222222222222222222222222222222222222222222'
            '2111111111111111111111111111111111111111111111111111100000000'
            '00000000000000000000000000000000000000000000\x0ctimestampvalT'
            '\x00\x00\x00\x00Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08arrayval'
            'A\x00\x00\x00\tU\x00\x01U\x00\x02U\x00\x03\x07dictvalF\x00\x00'
            '\x00\t\x03foos\x03bar')
    expectation = {'longval': 912598613,
                   'floatval': 3.140000104904175,
                   'strval': u'Test',
                   'intval': 1,
                   'timestampval': time.struct_time((2006, 11, 21, 16, 30, 10,
                                                     1, 325, 0)),
                   'longstr': (u'0000000000000000000000000000000000000000000'
                               u'0000000001111111111111111111111111111111111'
                               u'1111111111111111112222222222222222222222222'
                               u'2222222222222222222222222221111111111111111'
                               u'1111111111111111111111111111111111112222222'
                               u'2222222222222222222222222222222222222222222'
                               u'2211111111111111111111111111111111111111111'
                               u'1111111111122222222222222222222222222222222'
                               u'2222222222222222222211111111111111111111111'
                               u'1111111111111111111111111111122222222222222'
                               u'2222222222222222222222222222222222222211111'
                               u'1111111111111111111111111111111111111111111'
                               u'1111222222222222222222222222222222222222222'
                               u'2222222222222111111111111111111111111111111'
                               u'1111111111111111111111222222222222222222222'
                               u'2222222222222222222222222222222111111111111'
                               u'1111111111111111111111111111111111111111222'
                               u'2222222222222222222222222222222222222222222'
                               u'2222221111111111111111111111111111111111111'
                               u'1111111111111110000000000000000000000000000'
                               u'000000000000000000000000'),
                   'dictval': {'foo': u'bar'},
                   'boolval': True,
                   'arrayval': [1, 2, 3],
                   'decval': decimal.Decimal('3.14')}

    length, value = codec.decode.by_type(data, 'table')
    print value
    print expectation
    if not isinstance(value, dict):
        assert False, "decode.field_table did not return a dict: %r" % value
    test_support.compare_dicts(value, expectation, 'decode.field_table')


def test_decode_timestamp():
    value = '\x00\x00\x00\x00Ec)\x92'
    length, expectation = codec.decode.by_type(value, 'timestamp')
    if not isinstance(expectation, time.struct_time):
        assert False, \
            "decode.by_type did not return a struct_time: %r" % expectation
    if time.mktime(expectation) != \
       time.mktime((2006, 11, 21, 16, 30, 10, 1, 325, 0)):
        assert False, \
            ("decode.by_type did not return '2006, 11, 21"
             ", 16, 30, 10': %r" % expectation)


def test_decode_by_value_error():

    try:
        codec.decode.by_type('VALUE', 'GOOD')
    except ValueError:
        return
    assert False, 'decode.by_type did not raise ValueError for bad type'

# -- Encoding Tests --

