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


# FIXME: this utility function should move somewhere appropriate
def to_camel_case(string):
    # Transform name to CamelCase
    words = string.split('_')
    capwords = [word.capitalize() for word in words]

    return "".join(capwords)


class Patchboard(object):
    """
    The primary client interface to a patchboard server.
    """

    def __init__(self, api_spec):
        self.api = API(api_spec)

        self.schema_manager = SchemaManager(self.api.schemas)
        self.endpoint_classes = {}
        self.create_endpoint_classes()

    # TODO: This looks like it can be simplified
    def create_endpoint_classes(self):
        resource_classes = {}
        for resource_name, mapping in self.api.mappings.iteritems():
            schema = self.schema_manager.find_name(resource_name)

            cls = resource_classes.setdefault(
                resource_name,
                self.create_class(
                    resource_name,
                    mapping.resource,
                    schema,
                    mapping))
            self.endpoint_classes[resource_name] = cls

    def create_class(self, resource_name, definition, schema, mapping):
        # Cannot use unicode for class names
        class_name = to_camel_case(str(resource_name))

        class_parents = (object,)
        # TODO: fill in stub class definition
        class_body = """
def __init__(self):
    pass
        """
        class_dict = {}
        exec(class_body, globals(), class_dict)
        cls = type(class_name, class_parents, class_dict)
        return cls

    def spawn(self):
        pass
