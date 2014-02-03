import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pika import utils


class UtilsTests(unittest.TestCase):

    def test_is_callable_true(self):
        self.assertTrue(utils.is_callable(utils.is_callable))

    def test_is_callable_false(self):
        self.assertFalse(utils.is_callable(1))

    def test_is_string_str(self):
        self.assertTrue(utils.is_string('foo'))

    def test_is_string_bytes(self):
        self.assertTrue(utils.is_string(b'foo'))

    @unittest.skipIf(sys.version_info[0] == 3, 'No unicode obj in 3')
    def test_is_string_unicode(self):
        self.assertTrue(utils.is_string(unicode('foo')))

    def test_is_string_false_int(self):
        self.assertFalse(utils.is_string(123))

    def test_is_string_false_dict(self):
        self.assertFalse(utils.is_string({'foo': 'bar'}))

    def test_is_string_false_list(self):
        self.assertFalse(utils.is_string(['foo', 'bar']))
