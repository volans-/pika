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


def encode_connection_open_test():
    expectation = u'\x00\n\x00(\x01/\x00\x01'
    test_method = amqp.Connection.Open(virtual_host='/',
                                       capabilities='',
                                       insist=True)
    frame_data = test_method.encode()
    if frame_data != expectation:
        assert False, ("%s did not encode the frame as expected:\n%r\n%r" %
                       (test_method.__class__.__name__,
                        expectation, frame_data))
