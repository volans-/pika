# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-04-10'

import test_support

from pika import amqp


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


def test_protocol_header_marshal():
    frame_data = u'AMQP\x00\x00\t\x01'
    test = amqp.ProtocolHeader()
    if test.marshal() != frame_data:
        assert False, "ProtocolHeader frame did not match frame data sample"


def test_protocol_header_demarshal():
    # Raw Frame Data
    frame_data = u'AMQP\x00\x00\t\x01'

    # Decode the frame and validate lengths
    bytes_read, channel, test = amqp.frame.demarshal(frame_data)

    if test.__class__.__name__ != 'ProtocolHeader':
        assert False, "Invalid Frame Type: %s" % test.__class__.__name__

    if bytes_read != len(frame_data):
        assert False, "%s did not decode the proper number of bytes: %i:%i" %\
               (test.__class__.__name__, bytes_read, len(frame_data))

    if (test.major_version,
        test.minor_version,
        test.revision) != amqp.definitions.AMQP_VERSION:
        assert False, "Invalid Protocol Version: %i-%i-%i" % \
                      (test.major_version, test.minor_version, test.revision)

def test_connection_start_demarshal():
    frame_data = (u'\x01\x00\x00\x00\x00\x01G\x00\n\x00\n\x00\t\x00\x00\x01'
                  u'"\x0ccapabilitiesF\x00\x00\x00X\x12publisher_confirmst\x01'
                  u'\x1aexchange_exchange_bindingst\x01\nbasic.nackt\x01\x16'
                  u'consumer_cancel_notifyt\x01\tcopyrightS\x00\x00\x00'
                  u'$Copyright (C) 2007-2011 VMware, Inc.\x0binformationS\x00'
                  u'\x00\x005Licensed under the MPL.  See http://www.rabbitmq'
                  u'.com/\x08platformS\x00\x00\x00\nErlang/OTP\x07productS\x00'
                  u'\x00\x00\x08RabbitMQ\x07versionS\x00\x00\x00\x052.6.1\x00'
                  u'\x00\x00\x0ePLAIN AMQPLAIN\x00\x00\x00\x05en_US\xce')

    expectation = {'version_major': 0,
                   'version_minor': 9,
                   'server_properties':
                       {u'information': (u'Licensed under the MPL.  '
                                          'See http://www.rabbitmq.com/'),
                        u'product': u'RabbitMQ',
                        u'copyright': u'Copyright (C) 2007-2011 VMware, Inc.',
                        u'capabilities': {u'exchange_exchange_bindings': True,
                                          u'consumer_cancel_notify': True,
                                          u'publisher_confirms': True,
                                          u'basic.nack': True},
                      u'platform': u'Erlang/OTP',
                      u'version': u'2.6.1'},
                   'mechanisms': u'PLAIN AMQPLAIN',
                   'locales': u'en_US'}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the bytes consumed
    if consumed != 335:
        assert False, 'Bytes consumed did not match the expected value'

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)

def test_connection_tune_demarshal():
    frame_data = (u'\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1e\x00\x00\x00\x02'
                  u'\x00\x00\x00\x00\xce')

    expectation = {'channel_max': 0,
                   'frame_max': 131072,
                   'heartbeat': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the bytes consumed
    if consumed != 20:
        assert False, 'Bytes consumed did not match the expected value'

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)
