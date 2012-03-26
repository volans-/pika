"""
Global CallbackManager for a given connection

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-03-25'

import logging


class CallbackManager(object):
    """The callback manager is responsible for calling stored methods for given
    channel and AMQP frame types when the frame type is received off the
    socket and demarshaled.

    """
    def __init__(self):
        """Create an instance of CallbackManager initializing the callback
        stack dictionary.

        """
        self._logger = logging.getLogger(__name__)
        self._logger.debug('Created a new instance of CallbackManager')
        self._callbacks = {0: dict()}

    def add(self, channel, frame, callback):
        """Add the method specified to the callback data structure for the
        given channel and frame type.

        :param int channel: Channel number
        :param any frame: The frame obj or class to add the callback for
        :param function callback: The method to add the callback for

        """
        # Get the normalized frame type
        frame_type = self._normalize_frame_reference(frame)

        # Make sure the channel is in the callback stack
        self._use_channel(channel)

        # If the frame type does not have callbacks, setup an empty structure
        self._use_frame_type(channel, frame_type)

        # Append the method to the callback stack
        self._callbacks[channel][frame_type].append(callback)
        self._logger.debug('Appended %r to the %r callbacks for channel %r',
                           callback, frame_type, channel)

    def process(self, channel, frame):
        """Process the callbacks for the given frame.

        :param pika.amqp.frame.Frame frame: The frame to process

        """
        # Get the normalized frame type
        frame_type = self._normalize_frame_reference(frame)

        # Make sure the frame type is in the callback stack
        if not self._has_callback(channel, frame_type):
            return

        # Use each item from the stack
        while self._callbacks[channel][frame_type]:
            callback = self._get_callback(channel, frame_type)

            # Call the specified callback passing the frame object
            callback(frame)

        # Remove the callback list item from the stack
        del self._callbacks[channel][frame_type]

    def _get_callback(self, channel, frame_type):
        """Return the left most callback item in the stack for the given
        channel and frame_type.

        :param int channel: The channel for the given frame type
        :param str frame_type: The frame type to get the callback for
        :return: function

        """
        return self._callbacks[channel][frame_type].pop(0)

    def _has_callback(self, channel, frame_type):
        """Check to see if the callback stack has the given channel and
        frame_type.

        """
        self._use_channel(channel)
        return frame_type in self._callbacks[channel]

    def _normalize_frame_reference(self, obj):
        """Take the given object and return the value if it's a string or the
        type of object it is if not.

        :param any obj: The object to get the name of
        :return: str

        """
        self._logger.debug('Frame obj: %r', obj)
        return str(obj)

    def _use_channel(self, channel):
        """Prepare the data structures object to use the given channel by
        validating the channel is in the callback stack.

        :param int channel: The channel number

        """
        if not channel in self._callbacks:
            self._logger.debug('Creating data structure for channel %r',
                               channel)
            self._callbacks[channel] = dict()

    def _use_frame_type(self, channel, frame_type):
        """Prepare the callback data structure by adding the frame type
        to the callbacks stack as a list if it does not exist.

        :param int channel: The channel for the given frame type
        :param str frame_type: The frame type for to validate

        """
        if not frame_type in self._callbacks[channel]:
            self._logger.debug('Creating data structure for %r in channel %r',
                               channel, frame_type)
            self._callbacks[channel][frame_type] = list()
