# ***** BEGIN LICENSE BLOCK *****
#
# For copyright and licensing please refer to COPYING.
#
# ***** END LICENSE BLOCK *****

from setuptools import setup

long_description = """\
Pika is a pure-python RabbitMQ client library that supports multiple
methodologies for development including the utilization of common pythonic
idioms in addition to callback-passing-style development commonly found
in asynchronous development models. It is built on an asynchronous
communication foundation which allows for both stand-alone development and
easy integration with common asynchronous development frameworks such as
Tornado and Twisted. Pika supports Python 2.6 through 3.2.
"""

setup(name='pika',
      version='2.0.0',
      description='RabbitMQ client library',
      long_description=long_description,
      author='Tony Garnock-Jones, Gavin M. Roy',
      author_email='tonygarnockjones@gmail.com, gmr@myyearbook.com',
      url='http://pika.github.com/',
      packages=['pika',
                'pika.adapters',
                'pika.amqp',
                'pika.authentication',
                'pika.codec',
                'pika.interfaces'],
      extras_require={'Tornado' : ['tornado']},
      setup_requires=['nosexcover', 'mock', 'unittest2', 'coverage', 'pylint', 'pep8'],
      test_suite = "nose.collector",
      license='MPL v1.1 and GPL v2.0 or newer',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        ],
        zip_safe=True,
      )
