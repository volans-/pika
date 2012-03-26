"""
tornado.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

from pika.amqp import connection


class Tornado(connection.Broker):

    def __init__(self):
        pass
