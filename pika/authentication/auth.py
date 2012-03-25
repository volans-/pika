"""
Base Authentication Class

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'


#pylint: disable=R0921
class Auth(object):
    """Base class to be implemented by authentication classes"""
    DEFAULT_CREDENTIALS = ''

    def clear(self):
        """Clear the in-memory storage of the authentication credentials.

        :raises: NotImplementedError

        """
        raise NotImplementedError

    def marshal(self):
        """Marshall the credentials into the correct values for AMQP
        authentication.

        :return: str

        """
        return self.DEFAULT_CREDENTIALS
