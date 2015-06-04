patchboard-py: A Python client for Patchboard APIs


patchboard-py is still alpha code but is in active development. Bug reports and
patches welcome.


Install patchboard-py:

Ubuntu:

Prerequisites:

1. A python 2.7 or 3.4 environment. virtualenv suggested.

Installing:

Either install from PyPI:

    $ pip install patchboard

or clone the git repository and run setup.py:

    $ git clone https://github.com/patchboard/patchboard-py.git
    $ cd patchboard-py
    $ python setup.py install

(if you're not using a virtual environment, you may need to use sudo)

Testing:

To run the automated pytest suite with an example server:

    $ python setup.py test

Or you can run against your existing server with:

    $ python setup.py test -a "--host=your-host --port=80"

-a (--pytest-args) sends an argument string to pytest.
