# patchboard.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


import json

from api import API
from schema_manager import SchemaManager


def discover(url):
    """
    Retrieve the API definition from the given URL and construct
    a Patchboard to interface with it.
    """
    # Retrieve JSON data from server
    # Treat url like a file and read mock JSON for now
    with open(url, u"r") as file:
        api_spec = json.load(file)

    return Patchboard(api_spec)


class Patchboard(object):
    """
    The primary client interface to a patchboard server.
    """

    def __init__(self, api_spec):
        self.api = API(api_spec)

        self.schema_manager = SchemaManager(self.api.schemas)

        self.resource_classes = self.create_resource_classes()

        # Debugging only
        self.json = api_spec

    def create_resource_classes(self):
        resource_classes = {}
        for name, mapping in self.api.mappings.iteritems():
            resource_classes[name] = u"<aclass>"

        return resource_classes

    def spawn(self):
        pass
