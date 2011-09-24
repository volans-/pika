
class Frame(object):
    """Base Class for AMQP Methods which specifies the encoding and decoding
    behavior.

    """
    arguments = list()
    id = 0
    index = 0
    name = 'Frame'

    def demarshal(self, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param data: The binary encoded method data
        :type data: str

        """
        for argument in self.arguments:
            data_type = getattr(self.__class__, argument)
            consumed, value = codec.decode.by_type(data, data_type)
            setattr(self, argument, value)
            data = data[consumed:]

    def marshal(self):
        """
        Dynamically encode the frame by taking the list of attributes and
        encode them item by item getting the value form the object attribute
        and the data type from the class attribute.

        :returns: unicode

        """
        output = list()
        for argument in self.arguments:
            output.append(codec.encode.by_type(getattr(self,
                                                       argument),
                                               getattr(self.__class__,
                                                       argument)))
        return u''.join(output)
