patchboard-py: A Python client for Patchboard APIs


patchboard-py is still beta code but is in active development. Bug reports and
patches welcome.


Install:

1. Install a python 2.7 environment (the nicest way to do this is with pyenv
   and virtualenv).  It is developed under 2.7.7, and while it may work with
   earlier versions that is currently untested. The goal is compatibility with
   at least the 2.7 and perhaps the 2.6 series. If those versions don't fit
   your needs drop us a line and we can talk about it.

2. Make sure you've installed pip (Debian/Ubuntu: python-pip), or at least
   setuptools (python-setuptools) if you only plan to work from the source
   package.

3. Install patchboard from PyPI:

    $ pip install patchboard

   or instead install from the github repo
   (https://github.com/patchboard/patchboard-py) and run 'python setup.py
   install', or 'python setup.py develop' if you plan to work on the codebase
   yourself.
