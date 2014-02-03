from setuptools import setup
import os
import sys

# Base Requirements
requirements = ['pamqp']

# Conditionally include additional modules for docs
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    #requirements.append('pyev') Won't work if libev is not installed
    requirements.append('tornado')
    requirements.append('twisted')

# Conditional include unittest2 for versions of python < 2.7
tests_require = ['nose', 'mock', 'pyyaml']
if sys.version_info < (2, 7, 0):
    tests_require.append('unittest2')


setup(name='pika',
      version='0.10.0',
      description='Pure-Python RabbitMQ Client Library',
      long_description=open('README.rst').read(),
      maintainer='Gavin M. Roy',
      maintainer_email='gavinmroy@gmail.com',
      url='https://pika.readthedocs.org ',
      packages=['pika', 'pika.adapters'],
      package_data={'': ['LICENSE', 'README.rst']},
      license='MPL v2.0',
      install_requires=requirements,
      include_package_data=True,
      extras_require={'tornado': ['tornado'],
                      'twisted': ['twisted'],
                      'libev': ['pyev']},
      tests_require=tests_require,
      test_suite='nose.collector',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Communications',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'],
      zip_safe=True)
