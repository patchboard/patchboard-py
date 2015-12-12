# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

setup(name='patchboard',
      version='0.5.2',
      description='Python client for Patchboard APIs',
      url='http://github.com/patchboard/patchboard-py',
      author='Dustin Laurence',
      author_email='dustin@gem.co',
      maintainer='Matt Smith',
      maintainer_email='matt@gem.co',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests',
      ]),
      install_requires=[
          'requests',
          'future'
      ],
      tests_require=[
        'pytest',
      ],
      zip_safe=False
)
