# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

"""
AMQP Header Class Definitions

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-24'

import struct

from . import definitions


class ProtocolHeader(object):
    """Class that represents the AMQP Protocol Header"""

    def __init__(self, major_version=None, minor_version=None, revision=None):
        """Construct a Protocol Header frame object for the specified AMQP
        version.

        :param major_version: Major version number.
        :type major_version: int.
        :param minor_version: Minor version number.
        :type minor_version: int.
        :param revision: Revision number.
        :type revision: int.
        """
        self.major_version = major_version or definitions.AMQP_VERSION[0]
        self.minor_version = minor_version or definitions.AMQP_VERSION[1]
        self.revision = revision or definitions.AMQP_VERSION[2]

    def demarshal(self, data):
        """Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param data: The binary encoded method data
        :type data: unicode
        :returns: int byte count of data used to demarshal the frame
        :raises: ValueError

        """
        if data[0:4] == 'AMQP':
            try:
                (self.major_version,
                 self.minor_version,
                 self.revision) = struct.unpack('BBB', data[5:8])
            except struct.error:
                raise ValueError('Data did not match the ProtocolHeader '
                                 'format: %r', data)

            # All in we consume 8 bytes
            return 8

        # The first four bytes did not match
        raise ValueError('Data did not match the ProtocolHeader format: %r',
                         data)

    def marshal(self):
        """Return the full AMQP wire protocol frame data representation of the
        ProtocolHeader frame.

        :returns: unicode
        """
        return u'AMQP' + struct.pack('BBBB', 0,
                                     self.major_version,
                                     self.minor_version,
                                     self.revision)



