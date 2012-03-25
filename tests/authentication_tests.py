"""
test_auth.py

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2012-03-25'

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
sys.path.insert(0, '..')

from pika.authentication import auth
from pika.authentication import plain
from pika.amqp import specification


class AuthTests(unittest.TestCase):

    def setUp(self):
        self._auth = auth.Auth()

    def tearDown(self):
        del self._auth

    def test_clear(self):
        with self.assertRaises(NotImplementedError):
            self._auth.clear()

    def test_marshal(self):
        self.assertEqual(self._auth.marshal(), '')


class PlainAuth(unittest.TestCase):

    USER = 'TEST'
    PASS = 'PASS'

    def setUp(self):
        self._auth = plain.PlainAuth(self.USER, self.PASS)

    def tearDown(self):
        del self._auth

    def test_parameters(self):
        self.assertEqual(self._auth._username, self.USER)
        self.assertEqual(self._auth._password, self.PASS)

    def test_clear(self):
        self._auth.clear()
        self.assertEqual(self._auth._username, None)
        self.assertEqual(self._auth._password, None)

    def test_marshal(self):
        self.assertEqual(self._auth.marshal(),
                         '\0%s\0%s' % (self.USER, self.PASS))

    def test_defaults(self):
        auth_obj = plain.PlainAuth()
        self.assertEqual(auth_obj._username, specification.DEFAULT_USER)
        self.assertEqual(auth_obj._password, specification.DEFAULT_PASS)


def test_import():
    try:
        from pika.authentication import PlainAuth
    except ImportError:
        assert False, 'Could not import PlainAuth from pika.authentication'  
