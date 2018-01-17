#!/usr/bin/env python

from setuptools import setup, Command, Extension
import pytest
from os.path import splitext, basename, join as pjoin
import os, sys

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name = 'dbloader',
      version = '0.2.0',
      description = 'Database Load Testing',
      url = 'http://github.com/phil-hildebrand/dbloader',
      author = 'Phil Hildebrand',
      author_email = 'phil.hildebrand@gmail.com',
      license = 'mit',
      packages = ['dbloader', 'loader', 'mongo_loader', 'rethink_loader'],
      package_dir = {'dbloader': 'dbloader',
                     'loader': 'dbloader/loader',
                     'mongo_loader' : 'dbloader/mongo',
                     'rethink_loader' : 'dbloader/rethink'},
      install_requires = [ requirements ],
      test_suite="pytest",
      use_2to3=True
)
