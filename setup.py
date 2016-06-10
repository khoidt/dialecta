#!/usr/bin/env python

from setuptools import setup

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
  # See: http://stackoverflow.com/questions/23418735/using-python-3-3-in-openshifts-book-example?noredirect=1#comment35908657_23418735
  exec(compile(open(virtualenv, 'rb').read(), virtualenv, 'exec'), dict(__file__=virtualenv)) # for Python v3.3
  # Multi-Line for Python v3.3:
  exec_namespace = dict(__file__=virtualenv)
  with open(virtualenv, 'rb') as exec_file:
    file_contents = exec_file.read()
  compiled_code = compile(file_contents, virtualenv, 'exec')
  exec(compiled_code, exec_namespace)
except IOError:
  pass

setup(
    # GETTING-STARTED: set your app name:
    name='Dialects',
    # GETTING-STARTED: set your app version:
    version='1.0-alpha',
    # GETTING-STARTED: set your app description:
    description='OpenShift Django App',
    # GETTING-STARTED: set author name (your name):
    author='Ilya Khait',
    # GETTING-STARTED: set author email (your email):
    author_email='ekh.itd@gmail.com',
    # GETTING-STARTED: set author url (your url):
    url='http://www.python.org/sigs/distutils-sig/',
    # GETTING-STARTED: define required django version:
    install_requires=[
        'Django==1.8.4'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
