# patchboard.py
#
# Copyright 2014 BitVault.


import json

from api import API


def discover(url):
    """
    Retrieve the API definition from the given URL and construct
    a Patchboard to interface with it.
    """
    # Retrieve JSON data from server
    # Treat url like a file and read mock JSON for now
    with open(url, "r") as file:
        api_spec = json.load(file)

    return Patchboard(api_spec)


class Patchboard(object):
    """
    The primary client interface to a patchboard server.
    """

    def __init__(self, api_spec):
        self.api = API(api_spec)

        # Debugging only
        self.json = api_spec

    def spawn(self):
        pass
