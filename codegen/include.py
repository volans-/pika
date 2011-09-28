
class Frame(object):
    """Base Class for AMQP Methods which specifies the encoding and decoding
    behavior.

    """
    attributes = list()
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
        offset = 0
        processing_bitset = False
        for argument in self.attributes:

            data_type = getattr(self.__class__, argument)

            if offset == 7 and processing_bitset:
                data = data[1:]
                offset = 0

            if processing_bitset and data_type != 'bit':
                offset = 0
                processing_bitset = False
                data = data[1:]

            consumed, value = codec.decode.by_type(data, data_type, offset)

            if data_type == 'bit':
                offset += 1
                processing_bitset = True

            setattr(self, argument, value)
            if consumed:
                data = data[consumed:]

    def marshal(self):
        """
        Dynamically encode the frame by taking the list of attributes and
        encode them item by item getting the value form the object attribute
        and the data type from the class attribute.

        :returns: unicode

        """
        output = list()
        for argument in self.attributes:
            output.append(codec.encode.by_type(getattr(self,
                                                       argument),
                                               getattr(self.__class__,
                                                       argument)))
        return u''.join(output)



class PropertiesBase(object):
    """Provide a base object that marshals and demarshals the Basic.Properties
    object values.

    """

    attributes = list()
    flags = dict()
    name = 'PropertiesBase'

    def demarshal(self, flags, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param flags: Flags that indicate if the data has the given property
        :type flags: int
        :param data: The binary encoded method data
        :type data: unicode

        """
        flag_values = getattr(self.__class__, 'flags')
        for attribute in self.attributes:
            if flags & flag_values[attribute]:
                attribute = attribute.replace('-', '_')
                data_type = getattr(self.__class__, attribute)
                consumed, value = codec.decode.by_type(data, data_type)
                setattr(self, attribute, value)
                data = data[consumed:]
