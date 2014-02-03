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


# Namedtuple for urlparse result
Parsed = collections.namedtuple('Parsed',
                                'scheme,netloc,path,params,query,fragment,'
                                'username,password,hostname,port')


def parse_qs(query_string):
    """Wrap urlparse.parse_qs supporting Python 2.6, 2.7, 3.2, 3.3

    Parse a query string given as a string argument
    (data of type application/x-www-form-urlencoded). Data are returned as a
    dictionary. The dictionary keys are the unique query variable names and the
    values are lists of values for each name.

    :param bytes|str|unicode query_string: The query string to parse
    :return: dict

    """
    return _urlparse.parse_qs(query_string)


def urlparse(url):
    """Wrap urlparse.urlparse to support Python 2.6, 2.7, 3.2, and 3.3

    Parse a URL into six components, returning a 6-tuple. This corresponds to
    the general structure of a URL: scheme://netloc/path;parameters?query#frag.
    Each tuple item is a string, possibly empty. The components are not broken
    up in smaller parts (for example, the network location is a single string),
    and % escapes are not expanded. The delimiters as shown above are not part
    of the result, except for a leading slash in the path component, which is
    retained if present.

    :param bytes|str|unicode url: The URL to parse
    :return: namedtuple

    """
    value = 'http%s' % url[4:] if url[:4] == 'amqp' else url
    parsed = _urlparse.urlparse(value)
    return Parsed(parsed.scheme.replace('http', 'amqp'), parsed.netloc,
                  parsed.path, parsed.params, parsed.query, parsed.fragment,
                  parsed.username, parsed.password, parsed.hostname,
                  parsed.port)


def unquote(value):
    """Wrap urlparse.unquote to support Python 2.6, 2.7, 3.2, and 3.3

    Replace %xx escapes by their single-character equivalent.

    :param bytes|str|unicode value: The value to unquote
    :return: str

    """
    return _urlparse.unquote(value)
