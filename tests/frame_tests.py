# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-04-10'

import test_support
from pika.amqp import definitions as amqp
from pika import frame


def validate_method_frame(frame_handle, method):
    """
    Pass in a fully decoded frame object and it will validate that it is a
    method frame and return the frame.method object for additional test
    inspection.
    """
    pass


def validate_attribute(method, attribute, attribute_type, value='ignore'):
    """
    Validate that the given method object has the specified attribute of the
    specified attribute_type. If a value is passed in, validate that as well
    """
    if not hasattr(method.frame, attribute):
        assert False, "%s missing %s attribute" % (method.frame, attribute)

    if getattr(method.frame, attribute) and \
       not isinstance(getattr(method.frame, attribute), attribute_type):
        assert False, "%s.%s is not %s" % \
                      (method.frame, attribute, attribute_type)

    if value != 'ignore' and value != getattr(method.frame, attribute):
        assert False, "Expected a value of %r, received %r" % \
                      (value, getattr(method.frame, attribute))


def test_protocol_header_encode():
    frame_data = 'AMQP\x00\x00\t\x01'
    test = frame.ProtocolHeader()
    if test.encode() != frame_data:
        assert False, "ProtocolHeader frame did not match frame data sample"


def test_protocol_header_decode():
    # Raw Frame Data
    frame_data = 'AMQP\x00\x00\t\x01'

    # Decode the frame and validate lengths
    bytes_read, test = frame.decode_frame(frame_data)

    if test.__class__.__name__ != 'ProtocolHeader':
        assert False, "Invalid Frame Type: %s" % test.__class__.__name__

    if bytes_read != len(frame_data):
        assert False, "%s did not decode the proper number of bytes: %i:%i" %\
               (test.__class__.__name__, bytes_read, len(frame_data))

    if (test.major_version,
        test.minor_version,
        test.revision) != amqp.AMQP_VERSION:
        assert False, "Invalid Protocol Version: %i-%i-%i" % \
                      (test.major_version, test.minor_version, test.revision)


def decode_connection_open_test():

    frame_data = '\x01\x00\x00\x00\x00\x00\x08\x00\n\x00(\x01/\x00\x01\xce'

    # Decode our frame data and validate lengths
    bytes_read, test = frame.decode_frame(frame_data)

    if bytes_read != len(frame_data):
        assert False, "%s did not decode the proper number of bytes: %i:%i" %\
               (test.frame.__class__.__name__, bytes_read, len(frame_data))

    validate_attribute(test, 'insist', bool, True)
    validate_attribute(test, 'capabilities', str, '')
    validate_attribute(test, 'virtual_host', str, '/')


def decode_connection_tuneok_test():

    frame_data = '\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1f\x00\x00\x00\x02\x00\x00\x00\x00\xce'

    # Decode our frame data and validate lengths
    bytes_read, test = frame.decode_frame(frame_data)

    if bytes_read != len(frame_data):
        assert False, "%s did not decode the proper number of bytes: %i:%i" %\
               (test.frame.__class__.__name__, bytes_read, len(frame_data))

    # Verify it is a method frame and return frame.method
    method = validate_method_frame(test, amqp.Connection.TuneOk)

    # Validate the attributes
    validate_attribute(test, 'frame_max', int, 131072)
    validate_attribute(test, 'channel_max', int, 0)
    validate_attribute(test, 'heartbeat', int, 0)

decode_connection_tuneok_test()
decode_connection_open_test()
