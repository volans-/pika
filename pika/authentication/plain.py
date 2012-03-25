"""
plain.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

from pika.authentication import auth
from pika.amqp import specification


class PlainAuth(auth.Auth):
    """Class for specifying the credentials to connect with when using AMQP
    PlainAuth.

    """
    def __init__(self, username=None, password=None):
        """Create the PlainAuth object for authentication that defaults to the
        specification default user and default pass.

        :param str username: The username to connect as, if omitted uses
                             pika.amqp.specification.DEFAULT_USER
        :param str password: The password to connect with, if omitted, use
                             pika.amqp.specification.DEFAULT_PASS

        """
        self._username = username or specification.DEFAULT_USER
        self._password = password or specification.DEFAULT_PASS

    def marshal(self):
        """Return the marshaled auth credentials

        :returns str: The marshaled string

        """
        return '\0%s\0%s' % (self._username, self._password)
