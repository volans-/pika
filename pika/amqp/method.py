"""
AMQP Method Base Class

"""

__author__ = 'Gavin M. Roy <gmr@myyearbook.com>'
__since__ = '2011-09-23'

import struct

from pika import codec


class Method(object):

    arguments = list()
    id = 0
    index = 0

    @property
    def name(self):
        return self.__class__.__name__

    def encode(self):
        """
        Dynamically encode the frame by taking the list of attributes and
        encode them item by item getting the value form the object attribute
        and the data type from the class attribute.

        :returns: unicode

        """
        output = list()
        output.append(struct.pack('>I', self.__class__.index))

        print output
        for argument in self.arguments:
            output.append(codec.encode.by_type(getattr(self,
                                                       argument),
                                               getattr(self.__class__,
                                                       argument)))
        return u''.join(output)
