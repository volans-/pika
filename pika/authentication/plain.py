"""
plain.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

from . import auth


class PlainAuth(auth.Auth):

    def __init__(self, username, password):
        """Create the PlainAuth object that will

        """
        self._username = username
        self._password = password

    def marshal(self):
        """Return the marshaled auth credentials

        :returns str: The marshaled string
        """
        return '\0%s\0%s' % self._username, self._password
