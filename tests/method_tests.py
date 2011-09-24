# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-09-23'

import test_support
from pika.amqp import definitions as amqp


def decode_connection_open_test():
    data = u'\x04test\x00\x01'
    test_method = amqp.Connection.Open()
    test_method.decode(data)
    test_support.validate_attribute(test_method, 'insist', bool, True)
    test_support.validate_attribute(test_method, 'capabilities',
                                    basestring, '')
    test_support.validate_attribute(test_method, 'virtual_host',
                                    basestring, 'test')


def encode_connection_open_test():
    expectation = u'\x04test\x00\x01'
    test_method = amqp.Connection.Open(virtual_host='test',
                                       capabilities='',
                                       insist=True)
    frame_data = test_method.encode()
    if frame_data != expectation:
        assert False, ("%s did not encode the frame as expected:\n%r\n%r" %
                       (test_method.__class__.__name__,
                        expectation, frame_data))


def decode_connection_start_test():
    data = (u'\x00\t\x00\x00\x00!\x07products\x08RabbitMQ\x07version'
             's\x052.6.1\x00\x00\x00\x05PLAIN\x00\x00\x00\x05uk_UK')
    test_method = amqp.Connection.Start()
    test_method.decode(data)
    test_support.validate_attribute(test_method, 'version_major', int, 0)
    test_support.validate_attribute(test_method, 'version_minor', int, 9)
    test_support.validate_attribute(test_method,
                                    'server_properties',
                                    dict, {'product': 'RabbitMQ',
                                           'version': '2.6.1'})
    test_support.validate_attribute(test_method, 'mechanisms',
                                    basestring, 'PLAIN')
    test_support.validate_attribute(test_method, 'locales',
                                    basestring, 'uk_UK')


def encode_connection_start_test():
    expectation = (u'\x00\t\x00\x00\x00!\x07products\x08RabbitMQ\x07version'
                    's\x052.6.1\x00\x00\x00\x05PLAIN\x00\x00\x00\x05uk_UK')
    test_method = amqp.Connection.Start(0, 9, {'product': 'RabbitMQ',
                                               'version': "2.6.1"},
                                        'PLAIN', 'uk_UK')
    frame_data = test_method.encode()
    if frame_data != expectation:
        assert False, ("%s did not encode the frame as expected:\n%r\n%r" %
                       (test_method.__class__.__name__,
                        expectation, frame_data))

