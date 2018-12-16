#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='Coplen',
      version='1.0',
      description='Course Plan Generator',
      author='João Paulo Taylor Ienczak Zanette',
      author_email='jpaulotiz@gmail.com',
      url='https://github.com/jptiz/coplen',
      packages=find_packages(),
      install_requires=['carl', 'jinja2'],
      )
