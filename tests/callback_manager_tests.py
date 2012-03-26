"""
callback_manager_tests.py

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-03-25'

try:
    import unittest2 as unittest
except ImportError:
    import unittest
import mock
import sys
sys.path.insert(0, '..')

from pika import callback_manager


class CallbackManagerTests(unittest.TestCase):

    CHANNEL = 0
    FRAME_OBJ = 'Foo'

    def setUp(self):
        self._manager = callback_manager.CallbackManager()

    def tearDown(self):
        del self._manager

    def test_adding_callback(self):
        mock_method = mock.Mock()
        self._manager.add(self.CHANNEL, self.FRAME_OBJ, mock_method)
        self.assertEqual(self._manager._callbacks[self.CHANNEL][self.FRAME_OBJ][0],
                         mock_method)

    def test_process_callback(self):
        mock_method = mock.Mock()
        self._manager.add(self.CHANNEL, self.FRAME_OBJ, mock_method)
        self._manager.process(self.CHANNEL, self.FRAME_OBJ)
        self.assertTrue(mock_method.called)

    def test_process_callback_no_pending(self):
        self._manager.process(self.CHANNEL, self.FRAME_OBJ)

    def test_use_channel(self):
        self._manager._use_channel(1)
        self.assertTrue(isinstance(self._manager._callbacks[1], dict))

    def test_use_frame(self):
        self._manager._use_channel(self.CHANNEL)
        self._manager._use_frame_type(self.CHANNEL, self.FRAME_OBJ)
        self.assertTrue(isinstance(self._manager._callbacks[self.CHANNEL][self.FRAME_OBJ], list))
