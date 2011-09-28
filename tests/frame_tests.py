# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-04-10'

import time

import test_support
from pika import amqp


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
        test.revision) != amqp.specification.AMQP_VERSION:
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

    # Validate the frame name
    if frame.name != 'Connection.Start':
        assert False, \
            ('Frame was of wrong type, expected Connection.Start, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 334:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (334, consumed)

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

    # Validate the frame name
    if frame.name != 'Connection.Tune':
        assert False, \
            ('Frame was of wrong type, expected Connection.Tune, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (19, consumed)

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def test_connection_open_ok_demarshal():
    frame_data = (u'\x01\x00\x00\x00\x00\x00\x05\x00\n\x00)\x00\xce')

    expectation = {'known_hosts': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.OpenOk':
        assert False, \
            ('Frame was of wrong type, expected Connection.OpenOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 12:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (12, consumed)

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def test_channel_open_ok_demarshal():
    frame_data = (u'\x01\x00\x01\x00\x00\x00\x08\x00\x14\x00\x0b\x00\x00\x00'
                  u'\x00\xce')

    expectation = {'channel_id': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Channel.OpenOk':
        assert False, \
            ('Frame was of wrong type, expected Channel.OpenOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 15:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (15, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def test_queue_declare_ok_demarshal():
    frame_data = (u'\x01\x00\x01\x00\x00\x00\x11\x002\x00\x0b\x04test\x00\x00'
                  u'\x00\x00\x00\x00\x00\x00\xce')

    expectation = {'queue': 'test',
                   'message_count': 0,
                   'consumer_count': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.DeclareOk':
        assert False, \
            ('Frame was of wrong type, expected Queue.DeclareOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 24:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (24, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def test_channel_close_ok_demarshal():
    frame_data = (u'\x01\x00\x01\x00\x00\x00\x04\x00\x14\x00)\xce\x01\x00\x00'
                  u'\x00\x00\x00\x04\x00\n\x003\xce')

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Channel.CloseOk':
        assert False, \
            ('Frame was of wrong type, expected Channel.CloseOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (11, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

def test_basic_consume_ok_demarshal():
    frame_data = (u'\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x15\x07ctag1.0\xce')

    expectation = {'consumer_tag': 'ctag1.0'}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.ConsumeOk':
        assert False, \
            ('Frame was of wrong type, expected Basic.ConsumeOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (19, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def test_basic_deliver_demarshal():
    frame_data = (u'\x01\x00\x01\x00\x00\x00\x1b\x00<\x00<\x07ctag1.0\x00\x00'
                  u'\x00\x00\x00\x00\x00\x01\x00\x00\x04test\xce')

    expectation = {'consumer_tag': 'ctag1.0',
                   'delivery_tag': 1,
                   'redelivered': False,
                   'exchange': '',
                   'routing_key': 'test'}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Deliver':
        assert False, \
            ('Frame was of wrong type, expected Basic.Deliver, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 34:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (34, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def test_content_header_demarshal():
    frame_data = (u'\x02\x00\x01\x00\x00\x005\x00<\x00\x00\x00\x00\x00\x00\x00'
                  u'\x00\x00#\x90X\ntext/plain\x01\x00\x00\x00\x00N~I]\x05'
                  u'guest\x0cdemo_send.py\xce')

    expectation = {'class_id': 60,
                   'weight': 0,
                   'body_size': 35}

    properties = {'user_id': 'guest',
                  'timestamp': time.struct_time((2011,9,24,21,19,25,5,267,0)),
                  'delivery_mode': 1,
                  'app_id': 'demo_send.py',
                  'priority': None,
                  'headers': None,
                  'correlation_id': None,
                  'cluster_id': None,
                  'content_encoding': None,
                  'content_type': 'text/plain',
                  'reply_to': None,
                  'type': None,
                  'message_id': None,
                  'expiration': None}

    # Decode the frame and validate lengths
    consumed, channel, frame = amqp.frame.demarshal(frame_data)

    # Validate the bytes consumed
    if consumed != 61:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (61, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)

    # Run the frame check, assertions contained within
    test_support.check_frame(frame.properties, properties)


def test_content_body_demarshal():
    frame_data = (u'\x03\x00\x01\x00\x00\x00#Hello World #0:'
                  u'1316899165.75516605\xce')

    expectation = "Hello World #0:1316899165.75516605"

    # Decode the frame and validate lengths
    consumed, channel, data = amqp.frame.demarshal(frame_data)

    # Validate the bytes consumed
    if consumed != 41:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (41, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Validate the content
    if data != expectation:
        assert False, 'Content frame data did not match the expected value'
