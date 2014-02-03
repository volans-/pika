"""
Non-module specific functions shared by modules in the pika package

"""
import collections
try:
    from urllib import parse as _urlparse
except ImportError:
    import urlparse as _urlparse

from pamqp import PYTHON3


def is_callable(handle):
    """Returns a bool value if the handle passed in is a callable
    method/function

    :param any handle: The object to check
    :rtype: bool

    """
    return isinstance(handle, collections.Callable)


def is_string(value):
    """Evaluate a value and check to see if it's a string.

    :rtype: bool

    """
    checks = [isinstance(value, bytes), isinstance(value, str)]
    if not PYTHON3:
        checks.append(isinstance(value, unicode))
    return any(checks)


Parsed = collections.namedtuple('Parsed',
                                'scheme,netloc,path,params,query,fragment,'
                                'username,password,hostname,port')


def parse_qs(query_string):
    return _urlparse.parse_qs(query_string)


def urlparse(url):
    value = 'http%s' % url[4:] if url[:4] == 'amqp' else url
    parsed = _urlparse.urlparse(value)
    return Parsed(parsed.scheme.replace('http', 'amqp'), parsed.netloc,
                  parsed.path, parsed.params, parsed.query, parsed.fragment,
                  parsed.username, parsed.password, parsed.hostname,
                  parsed.port)


def unquote(value):
    return _urlparse.unquote(value)
