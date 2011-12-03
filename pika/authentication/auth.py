# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""
Base Authentication Object

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'


class Auth(object):

    def marshal(self):
        """
        Validate that our type of authentication is supported
        """
        return None
