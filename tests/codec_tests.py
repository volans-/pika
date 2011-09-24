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
from decimal import Decimal
from time import mktime, struct_time

# -- Helpers --

def compare_lists(source, dest, method='Unknown'):
    for position in xrange(0, len(source)):

        # Validate decimal, int, long, str, nothing special needed
        if isinstance(source[position], Decimal) or \
           isinstance(source[position], int) or \
           isinstance(source[position], long) or \
           isinstance(source[position], str):
            if source[position] != dest[position]:
                assert False, \
                "%s did not properly decode item in position %i '%r' vs '%r'" \
                % (method, position, source[position], dest[position])

        elif isinstance(source[position], float):
            if round(source[position], 2) != round(dest[position], 2):
                assert False, \
                "%s did not properly decode item in position %i '%r' vs '%r'" \
                % (method, position, source[position], dest[position])

        elif isinstance(source[position], struct_time):
            if mktime(source[position]) != mktime(dest[position]):
                assert False, \
                "%s did not properly decode item in position %i '%r' vs '%r'" \
                % (method, position, source[position], dest[position])

        elif isinstance(source[position], list):
            compare_lists(source[position], dest[position], method)

        elif isinstance(source[position], dict):
            compare_dicts(source[position], dest[position], method)

        else:
            assert False, "Unchecked item in position %i: %r" % \
                          (position, source[position])


def compare_dicts(source, dest, method='Unknown'):

    for key in source.keys():

        # Validate we have the key
        if key not in dest:
            assert False, "%s did not properly decode dict: %s missing: %r" % \
                          (method, key, dest)

        # Validate decimal, int, long, str, nothing special needed
        if isinstance(source[key], Decimal) or \
           isinstance(source[key], int) or \
           isinstance(source[key], long) or \
           isinstance(source[key], str):
            if source[key] != dest[key]:
                assert False, \
                "%s did not properly decode item %s '%r' vs '%r'" \
                % (method, key, source[key], dest[key])

        elif isinstance(source[key], float):
            if round(source[key], 2) != round(dest[key], 2):
                assert False, \
                "%s did not properly decode item %s '%r' vs '%r'" \
                % (method, key, source[key], dest[key])

        elif isinstance(source[key], struct_time):
            if mktime(source[key]) != mktime(dest[key]):
                assert False, \
                "%s did not properly decode item %s '%r' vs '%r'" \
                % (method, key, source[key], dest[key])

        elif isinstance(source[key], list):
            compare_lists(source[key], dest[key], method)

        elif isinstance(source[key], dict):
            compare_dicts(source[key], dest[key], method)

        else:
            assert False, "Unchecked item %s: %r" % \
                          (key, source[key])

# -- Decoding Tests --

def test_decode_none():
    length, check = codec.decode._decode_value('\x00')
    if check is not None:
        assert False, "decode._decode_value did not return None: %r" % check


def test_decode_unknown():
    try:
        codec.decode._decode_value('Z\x00')
    except ValueError:
        return
    assert False, "decode._decode_value did not raise a ValueError Exception"


def test_decode_by_type_unknown():
    try:
        codec.decode.decode_by_type('Z\x00', 'foobar')
    except ValueError:
        return
    assert False, "decode.decode_by_type did not raise a ValueError Exception"


def test_decode_bool_false():
    value = '\x00'
    length, check = codec.decode.boolean(value)
    if not isinstance(check, bool):
        assert False, "decode.boolean did not return a bool: %r" % check
    if check:
        assert False, "decode.boolean did not return False: %r" % check


def test_decode_bool_true():
    value = '\x01'
    length, check = codec.decode.boolean(value)
    if not isinstance(check, bool):
        assert False, "decode.boolean did not return a bool: %r" % check
    if not check:
        assert False, "decode.boolean did not return True: %r" % check


def test_decode_decimal():
    value = '\x05\x00\x04\xcb/'
    length, check = codec.decode.decimal(value)
    if not isinstance(check, Decimal):
        assert False, "decode.decimal did not return a Decimal: %r" % check
    if check != Decimal('3.14159'):
        assert False, "decode.decimal did not return 3.14159: %r" % check


def test_decode_float():
    value = '@I\x0f\xd0'
    length, check = codec.decode.floating_point(value)
    if not isinstance(check, float):
        assert False, "decode.floating_point did not return a float: %r" % \
                      check
    if round(check, 5) != 3.14159:
        assert False, "decode.floating_point did not return 3.14159: %r" % \
                      round(check, 5)


def test_decode_long():
    value = '\x7f\xff\xff\xff'
    length, check = codec.decode.long_int(value)
    if not isinstance(check, int) and not isinstance(check, long):
        assert False, "decode.long_int did not return an int: %r" % check
    if check != 2147483647:
        assert False, "decode.long_int did not return 2147483647: %r" % \
                      check


def test_decode_by_type_long():
    value = '\x7f\xff\xff\xff\xff\xff\xff\xf8'
    length, check = codec.decode.decode_by_type(value, 'longlong')
    if not isinstance(check, int) and not isinstance(check, long):
        assert False, "decode.long_int did not return an int: %r" % check
    if check != 9223372036854775800:
        assert False, \
                "decode.long_int did not return 9223372036854775800: %r" % \
                check


def test_decode_long_long():
    value = '\x7f\xff\xff\xff\xff\xff\xff\xf8'
    length, check = codec.decode.long_long_int(value)
    if not isinstance(check, int) and not isinstance(check, long):
        assert False, "decode.long_int did not return an int: %r" % check
    if check != 9223372036854775800:
        assert False, \
        "decode.long_long_int did not return 9223372036854775800: %r" % check


def test_decode_short():
    value = '\x7f\xff'
    length, check = codec.decode.short_int(value)
    if not isinstance(check, int):
        assert False, "decode.short_int did not return an int: %r" % check
    if check != 32767:
        assert False, "decode.short_int did not return 32767: %r" % check


def test_decode_long_string():
    value = '\x00\x00\x00\n0123456789'
    length, check = codec.decode.long_string(value)
    if not isinstance(check, basestring):
        assert False, "decode.long_string did not return a str: %r" % check
    if check != '0123456789':
        assert False, \
            "decode.long_string did not return '0123456789': %r" % check

def test_decode_by_type_long_string():
    value = '\x00\x00\x00\n0123456789'
    length, check = codec.decode.decode_by_type(value, 'longstr')
    if not isinstance(check, basestring):
        assert False, "decode.decode_by_type did not return a str: %r" % check
    if check != '0123456789':
        assert False, \
            "decode.decode_by_type did not return '0123456789': %r" % check

def test_decode_value_short_string():
    value = 's\n0123456789'
    length, check = codec.decode._decode_value(value)
    if not isinstance(check, basestring):
        assert False, "decode._decode_value did not return a str: %r" % check
    if check != '0123456789':
        assert False, \
            "decode._decode_value did not return '0123456789': %r" % check


def test_decode_short_string():
    value = '\n0123456789'
    length, check = codec.decode.short_string(value)
    if not isinstance(check, basestring):
        assert False, "decode.short_string did not return a str: %r" % check
    if check != '0123456789':
        assert False, \
            "decode.short_string did not return '0123456789': %r" % check


def test_decode_timestamp():
    value = '\x00\x00\x00\x00Ec)\x92'
    length, check = codec.decode.timestamp(value)
    if not isinstance(check, struct_time):
        assert False, "decode.timestamp did not return a struct_time: %r" % \
                      check
    if mktime(check) != mktime((2006, 11, 21, 16, 30, 10, 1, 325, 0)):
        assert False, \
        "decode.timestamp did not return '2006, 11, 21, 16, 30, 10': %r" % \
        check


def test_decode_by_type_timestamp():
    value = '\x00\x00\x00\x00Ec)\x92'
    length, check = codec.decode.decode_by_type(value, 'timestamp')
    if not isinstance(check, struct_time):
        assert False, \
            "decode.decode_by_type did not return a struct_time: %r" % check
    if mktime(check) != mktime((2006, 11, 21, 16, 30, 10, 1, 325, 0)):
        assert False, ("decode.decode_by_type did not return '2006, "
                       "11, 21, 16, 30, 10': %r" % check)


def test_decode_field_array():
    value = '\x00\x00\x00<U\x00\x01I\x00\x00\xaf\xc8S\x00\x00\x00\x04TestT\
\x00\x00\x00\x00Ec)\x92I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H\xf5\xc3L\x00\x00\
\x00\x00\xc4e5\xffL\x80\x00\x00\x00\x00\x00\x00\x08'
    data = [1, 45000, 'Test',  datetime(2006, 11, 21, 16, 30, 10).timetuple(),
            -1147483648, Decimal('3.14'), 3.14, long(3294967295),
            -9223372036854775800]
    length, check = codec.decode.field_array(value)
    if not isinstance(check, list):
        assert False, "decode.field_array did not return a list: %r" % check
    compare_lists(data, check, 'decode.field_array')


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
            'decval': Decimal('3.14'),
            'floatvla': 3.14,
            'longval': long(912598613),
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3]}
    length, check = codec.decode.field_table(value)
    if not isinstance(check, dict):
        assert False, "decode.field_table did not return a dict: %r" % check
    compare_dicts(data, check, 'decode.field_table')


def test_decode_field_table_by_type():
    value = '\x00\x00\x00\x92\x07longvalI6e&U\x08floatvlaf@H\xf5\xc3\x07\
boolvalt\x01\x06strvalS\x00\x00\x00\x04Test\x06intvalU\x00\x01\x0ctimestampval\
T\x00\x00\x00\x00Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08arrayvalA\x00\x00\x00\
\tU\x00\x01U\x00\x02U\x00\x03\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00\x00\
\x03bar'
    data = {'intval': 1,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime(2006, 11, 21, 16, 30, 10).timetuple(),
            'decval': Decimal('3.14'),
            'floatvla': 3.14,
            'longval': long(912598613),
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3]}
    length, check = codec.decode.decode_by_type(value, 'table')
    if not isinstance(check, dict):
        assert False, "decode.field_table did not return a dict: %r" % check
    compare_dicts(data, check, 'decode.field_table')

# -- Encoding Tests --

def test_encode_bool_wrong_type():
    try:
        codec.encode.boolean('Hi')
    except ValueError:
        return
    assert False, "encode.boolean did not raise a ValueError Exception"


def test_encode_bool_false():
    check = 't\x00'
    value = codec.encode.boolean(False)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_bool_true():
    check = 't\x01'
    value = codec.encode.boolean(True)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_decimal_wrong_type():
    try:
        codec.encode.decimal(3.141597)
    except ValueError:
        return
    assert False, "encode.decimal did not raise a ValueError Exception"


def test_encode_decimal():
    check = 'D\x05\x00\x04\xcb/'
    value = codec.encode.decimal(Decimal('3.14159'))
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_decimal_whole():
    check = 'D\x00\x00\x04\xcb/'
    value = codec.encode.decimal(Decimal('314159'))
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_floating_point_type():
    try:
        codec.encode.floating_point("1234")
    except ValueError:
        return
    assert False, "encode.float did not raise a ValueError Exception"


def test_encode_float():
    check = 'f@I\x0f\xd0'
    value = codec.encode.floating_point(float(3.14159))
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_long_int_wrong_type():
    try:
        codec.encode.long_int(3.141597)
    except ValueError:
        return
    assert False, "encode.long_int did not raise a ValueError Exception"


def test_encode_long_int():
    check = 'I\x7f\xff\xff\xff'
    value = codec.encode.long_int(long(2147483647))
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_long_int_error():
    try:
        codec.encode.long_int(long(21474836449))
    except ValueError:
        return
    assert False, "encode.long_int did not raise a ValueError Exception"


def test_encode_long_long_int_wrong_type():
    try:
        codec.encode.long_long_int(3.141597)
    except ValueError:
        return
    assert False, "encode.long_long_int did not raise a ValueError Exception"


def test_encode_long_long_int():
    check = 'L\x7f\xff\xff\xff\xff\xff\xff\xf8'
    value = codec.encode.long_long_int(long(9223372036854775800))
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_long_long_int_error():
    try:
        codec.encode.long_long_int(long(9223372036854775808))
    except ValueError:
        return
    assert False, "encode.long_long_int did not raise a ValueError Exception"


def test_encode_short_wrong_type():
    try:
        codec.encode.short_int(3.141597)
    except ValueError:
        return
    assert False, "encode.short_int did not raise a ValueError Exception"


def test_encode_short():
    check = 'U\x7f\xff'
    value = codec.encode.short_int(32767)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_integer_error():
    try:
        codec.encode._encode_integer(9223372036854775808)
    except ValueError:
        return
    assert False, "encode._encode_integer did not raise a ValueError Exception"


def test_encode_short_error():
    try:
        codec.encode.short_int(32768)
    except ValueError:
        return
    assert False, "encode.short_int did not raise a ValueError Exception"


def test_encode_long_string():
    check = 'S\x00\x00\x00\n0123456789'
    value = codec.encode.long_string("0123456789")
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_long_string_error():
    try:
        codec.encode.long_string(100)
    except ValueError:
        return
    assert False, "encode.long_string failed to raise a ValueError Exception"


def test_encode_short_string():
    check = 's\n0123456789'
    value = codec.encode.short_string("0123456789")
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value

def test_encode_unicode():
    check = 's\n0123456789'
    value = codec.encode.short_string(unicode("0123456789"))
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_string_error():
    try:
        codec.encode.short_string(12345.12434)
    except ValueError:
        return
    assert False, "encode.string did not raise a ValueError Exception"


def test_encode_timestamp_from_datetime():
    check = 'T\x00\x00\x00\x00Ec)\x92'
    value = datetime(2006, 11, 21, 16, 30, 10)
    value = codec.encode.timestamp(value)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_timestamp_from_struct_time():
    check = 'T\x00\x00\x00\x00Ec)\x92'
    value = datetime(2006, 11, 21, 16, 30, 10).timetuple()
    value = codec.encode.timestamp(value)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_timestamp_error():
    try:
        codec.encode.timestamp("hi")
    except ValueError:
        return
    assert False, "encode.timestamp did not raise a ValueError Exception"


def test_encode_field_array_error():
    try:
        codec.encode.field_array("hi")
    except ValueError:
        return
    assert False, "encode.field_array did not raise a ValueError Exception"


def test_encode_field_array():
    check = 'A\x00\x00\x009U\x00\x01I\x00\x00\xaf\xc8s\x04TestT\x00\x00\x00\
\x00Ec)\x92I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H\xf5\xc3L\x00\x00\x00\x00\
\xc4e5\xffL\x80\x00\x00\x00\x00\x00\x00\x08'

    data = [1, 45000, 'Test', datetime(2006, 11, 21, 16, 30, 10),
            -1147483648, Decimal('3.14'), 3.14, long(3294967295),
            -9223372036854775800]
    value = codec.encode.field_array(data)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_field_table_value_type_error():
    try:
        codec.encode.field_table({'test': object()})
    except ValueError:
        return
    assert False, "encode.field_table did not raise a ValueError Exception"


def test_encode_field_table_empty():
    value = codec.encode.field_table(None)
    if value != '\x00\x00\x00\x00':
        assert False, "Encoded value does not match check value: %r" % value


def test_encode_field_table_type_error():
    try:
        codec.encode.field_table([1, 2, 3])
    except ValueError:
        return
    assert False, "encode.field_table did not raise a ValueError Exception"


def test_encode_field_table():
    check = 'F\x00\x00\x00\x8c\x07longvalI6e&U\x08floatvlaf@H\xf5\xc3\x07\
boolvalt\x01\x06strvals\x04Test\x06intvalU\x00\x01\x0ctimestampvalT\x00\x00\
\x00\x00Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08arrayvalA\x00\x00\x00\tU\x00\
\x01U\x00\x02U\x00\x03\x07dictvalF\x00\x00\x00\t\x03foos\x03bar'
    data = {'intval': 1,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime(2006, 11, 21, 16, 30, 10),
            'decval': Decimal('3.14'),
            'floatvla': 3.14,
            'longval': long(912598613),
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3]}
    value = codec.encode.field_table(data)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value

def test_encode_value_large_str():
    check = ('S\x00\x00\x03\x1601234567891011121314151617181920212223242526272'
             '8293031323334353637383940414243444546474849505152535455565758596'
             '0616263646566676869707172737475767778798081828384858687888990919'
             '2939495969798991001011021031041051061071081091101111121131141151'
             '1611711811912012112212312412512612712812913013113213313413513613'
             '7138139140141142143144145146147148149150151152153154155156157158'
             '1591601611621631641651661671681691701711721731741751761771781791'
             '8018118218318418518618718818919019119219319419519619719819920020'
             '1202203204205206207208209210211212213214215216217218219220221222'
             '2232242252262272282292302312322332342352362372382392402412422432'
             '4424524624724824925025125225325425525625725825926026126226326426'
             '5266267268269270271272273274275276277278279280281282283284285286'
             '287288289290291292293294295296297298299')
    data = ''.join([str(position) for position in range(300)])
    value = codec.encode._encode_value(data)
    if value != check:
        assert False, "Encoded value does not match check value: %r" % value
