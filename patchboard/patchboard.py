# patchboard.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


import json

from resource import ResourceType
from api import API
from schema_manager import SchemaManager
from client import Client
from util import to_camel_case


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
        self.endpoint_classes = self.create_endpoint_classes()
        client = self.spawn()
        # Appears to be unused
        #self.resources = client.resources
        self.context = client.context

    def create_endpoint_classes(self):
        classes = {}
        for resource_name, mapping in self.api.mappings.iteritems():
            if resource_name not in classes:
                schema = self.schema_manager.find_name(resource_name)
                resource_def = mapping.resource
                cls = self.create_class(
                    resource_name,
                    resource_def,
                    schema,
                    mapping)
                classes[resource_name] = cls

        return classes

    def create_class(self, resource_name, definition, schema, mapping):
        # Cannot use unicode for class names
        class_name = to_camel_case(str(resource_name))

        cls = ResourceType(class_name)
        return cls

    def spawn(self, context={}):
        return Client(context, self.api, self.endpoint_classes)
