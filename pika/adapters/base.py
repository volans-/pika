# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****
"""
A Base IOLoop that may be extended by others

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import hashlib
import logging

# Use epoll's constants to keep life easy
READ = 0x0001
WRITE = 0x0004
ERROR = 0x0008


class IOLoop(object):

    def __init__(self):
        """Create an IOLoop object."""
        self._logger = logging.getLogger(__name__)
        self._file_descriptors = set()
        self._deadlines = dict()
        self._events = dict()

    def add_timeout(self, deadline, callback):
        """Add a timeout to the IOLoop returning an ID for the specific
        timeout event which may be referenced for removal or logging purposes.

        :param int deadline: Add timeout event that executes the
                             callback when deadline is reached
        :param method callback: Method to call when the deadline is reached
        :returns str: Timeout ID

        """
        self._logger.error('IOLoop.add_timeout called without being extended')

    def remove_timeout(self, timeout_id):
        """Remove a timeout to the IOLoop

        :param str timeout_id: The timeout ID to remove from the IOLoop if
                               the timeout has not fired yet
        :returns bool: Success/failure

        """
        self._logger.error('IOLoop.remove_timeout called without being '
                           'extended')
        return False

    def start(self):
        """Start the IOLoop"""
        self._logger.error('IOLoop.start called without being extended')

    def stop(self):
        """Start the IOLoop"""
        self._logger.error('IOLoop.start called without being extended')

    def set_events(self, file_descriptor, event_mask):
        """Pass in the events to process

        :param int file_descriptor: The file descriptor to set events for
        :param int event_mask: A bitmask of the events to register

        """
        self._logger.error('IOLoop.set_events called without being extended')

    def _get_timeout_id(self, deadline, callback):
        """Returns an ID specific to the callback.

        :param int deadline: The deadline for the callback
        :param method callback: The callback that will be executed
        :returns str: The timeout to use

        """
        timeout_id = hashlib.md5()
        timeout_id.update('%i-%r', deadline, callback)
        return str(timeout_id.hexdigest())
