# patchboard.py
#
# Copyright 2014 BitVault.


def discover(url):
    """
    Retrieve the API definition from the given URL and construct
    a Patchboard to interface with it.
    """

    return Patchboard()


class Patchboard(object):
    """
    The primary interface to a patchboard server.
    """

    def __init__(self):
        pass

    def spawn(self):
        return "a client object"
