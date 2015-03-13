# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        errno = 0
        if u"host" not in self.pytest_args:
            import sys,subprocess
            errno = subprocess.call([sys.executable, "patchboard/tests/scripts/play.py"])
            if errno > 0:
                raise SystemExit(errno)
        import pytest
        errno = max(errno, pytest.main(self.pytest_args))
        raise SystemExit(errno)

setup(name='patchboard',
      version='0.5.0',
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
      install_requires=['requests'],
      tests_require=[
        'pytest',
        ],
      cmdclass = {'test': PyTest},
      zip_safe=False
      )
