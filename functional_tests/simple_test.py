"""
Test use of the simple interface

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-10-16'

import sys
sys.path.insert(0, '..')
import logging
import pika

logging.basicConfig(level=logging.DEBUG)
rabbitmq = pika.Broker()
rabbitmq.open()
