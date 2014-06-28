patchboard-py: A Python client for Patchboard APIs


patchboard-py is still alpha code but is in active development. Bug reports and
patches welcome.


Install patchboard-py:

Ubuntu:

Prerequisites:

1. A python 2.7 environment (your distro probably does this as part of the base
   system, but the nicer way is with pyenv and/or virtualenv). patchboard-py is
   currently developed under 2.7.7.

Installing:

Either install from PyPI:

    $ sudo pip install patchboard

or clone the git repository and run setup.py:

    $ git clone https://github.com/patchboard/patchboard-py.git
    $ cd patchboard-py
    $ sudo python setup.py install

(if you're using a virtual environment, you obviously don't need sudo in
either case)
