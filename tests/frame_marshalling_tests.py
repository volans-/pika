# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-09-28'

import test_support
from pika import amqp


def marshal_protocol_header_test():

    # Decode the frame and validate lengths
    expectation = 'AMQP\x00\x00\t\x01'
    frame = amqp.ProtocolHeader()
    data = frame.marshal()

    if data != expectation:
        assert False, \
            "marshalling did not return the expectation: %r/%r" % \
            (data, expectation)
