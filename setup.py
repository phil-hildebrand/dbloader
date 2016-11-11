#!/usr/bin/env python

from setuptools import setup, Command, Extension
import unittest
from os.path import splitext, basename, join as pjoin
import os, sys

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name = 'dbloader',
      version = '0.1.0',
      description = 'Database Load Testing',
      url = 'http://github.com/phil-hildebrand/dbloader',
      author = 'Phil Hildebrand',
      author_email = 'phil.hildebrand@gmail.com',
      license = 'mit',
      packages = ['tests'],
      install_requires = [ requirements ],
      test_suite="tests",
      use_2to3=True
)
