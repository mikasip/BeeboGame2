#!/usr/bin/env python

from distutils.core import setup

setup(name='Beebo',
      version='1.0',
      description='Cool Beebo game',
      author='Mika Sipilä',
      author_email='mikasip11@gmail.com',
      url='-',
      install_requires=['pygame', 'jsonpickle', 'pytmx', 'numpy', 'python-dotenv']
     )