"""
select_adapter.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import select
from . import base


class SelectIOLoop(base.IOLoop):
    """A SelectIOLoop for notifications of read, write and error events."""
    ERROR = base.ERROR
    READ = base.READ
    WRITE = base.WRITE

    # select.select timeout
    TIMEOUT = 1

    def __init__(self):
        """Create an IOLoop object."""
        base.IOLoop.__init__(self)

        # By default the IOLoop is not running
        self._running = False

    def add_timeout(self, deadline, callback):
        """Add a timeout to the IOLoop returning an ID for the specific
        timeout event which may be referenced for removal or logging purposes.

        :param int deadline: Add timeout event that executes the
                             callback when deadline is reached
        :param method callback: Method to call when the deadline is reached
        :returns str: Timeout ID

        """
        self._logger.debug('Adding timeout at %i calling %r',
                           deadline, callback)

        # Create the timeout id for this event
        timeout_id = self._get_timeout_id(deadline, callback)

        # Add it to our stack
        self._deadlines[timeout_id] = callback

        # Return the timeout id to the invoker
        return timeout_id

    def remove_timeout(self, timeout_id):
        """Remove a timeout to the IOLoop

        :param str timeout_id: The timeout ID to remove from the IOLoop if
                               the timeout has not fired yet
        :returns bool: Success/failure

        """
        # Make sure the timeout is in the deadline stack
        if timeout_id in self._deadlines:
            self._logger.debug('Removing timeout_id %s', timeout_id)
            del self._deadlines[timeout_id]
            return True

        self._logger.debug('timeout_id %s not found in deadline stack',
                           timeout_id)
        return False

    def _poll(self):
        """Poll select to see what events we should process"""

        # Create empty lists to check for events on
        input_events, output_events, error_events = list(), list(), list()

        # Iterate through the sockets on in our events
        for file_descriptor in self._events:

            # Check to see if the file descriptor needs a read event
            if self._events[file_descriptor]['event_mask'] & base.READ:
                input_events.append(file_descriptor)

            # Check to see if the file descriptor needs a write event
            if self._events[file_descriptor]['event_mask'] & base.WRITE:
                output_events.append(file_descriptor)

            # Check to see if the file descriptor needs an error event
            if self._events[file_descriptor]['event_mask'] & base.ERROR:
                error_events.append(file_descriptor)

        # Wait on select to let us know what's up
        try:
            (read_events,
             write_events,
             error_events) = select.select(input_events,
                                           output_events,
                                           error_events,
                                           SelectIOLoop.TIMEOUT)
        except select.error as error:
            self._logger.error('Select error: %r', error)
            return

        # Iterate through each of the file descriptors in the read events
        for file_descriptor in read_events:
            # If the file descriptor has an event
            if file_descriptor in self._events:
                # Call the read method for the socket_io object
                self._events[file_descriptor]['socket_io'].read()

        # Iterate through each of the file descriptors in the write events
        for file_descriptor in write_events:
            # If the file descriptor has an event
            if file_descriptor in self._events:
                # Call the write method for the socket_io object
                self._events[file_descriptor]['socket_io'].write()

        # Iterate through each of the file descriptors in the error events
        for file_descriptor in error_events:
            # If the file descriptor has an event
            if file_descriptor in self._events:
                # Call the error method for the socket_io object
                self._events[file_descriptor]['socket_io'].error()

    def start(self):
        """Start the IOLoop"""
        self._logger.error('Starting the Select IOLoop')

        # Loop and rely on Select to let us know what to do
        while self._running:

            # Poll the select loop
            self._poll()

            # Evaluate the timeouts

    def stop(self):
        """Start the IOLoop"""
        self._logger.debug('Stopping SelectIOLoop')
        self._running = False

    def set_events(self, socket_io, event_mask):
        """Pass in the events to process

        :param pika.amqp.io.SocketIO: The SocketIO object for events
        :param int event_mask: A bitmask of the events to register

        """
        self._logger.debug('Setting events for fd %r: %i',
                           socket_io, event_mask)

        # Make sure the file_descriptor is in our file_descriptor stack
        self._events[socket_io.file_descriptor] = {'event_mask': event_mask,
                                                   'socket_io': socket_io}
