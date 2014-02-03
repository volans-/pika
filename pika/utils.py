"""
Non-module specific functions shared by modules in the pika package

"""
import collections

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
