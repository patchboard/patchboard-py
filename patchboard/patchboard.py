# patchboard.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


import requests

from resource import ResourceType
from api import API
from schema_manager import SchemaManager
from client import Client
from util import to_camel_case
from exception import PatchboardError


def discover(url):
    """
    Retrieve the API definition from the given URL and construct
    a Patchboard to interface with it.
    """
    # Retrieve API definition from server
    try:
        resp = requests.get(url, headers={u'Accept': u'application/json'})
    except Exception as e:
        raise PatchboardError("Problem discovering API: {0}".format(e))

    # Parse as JSON
    try:
        # Using the built-in requests json parser--find out if it
        # is different code than the json package, if so we may have
        # consistency issues.
        api_spec = resp.json()
    except Exception as e:
        raise PatchboardError("Unparseable API description: {0}".format(e))

    # Return core handle object
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
                class_name = to_camel_case(str(resource_name))
                cls = ResourceType(
                    class_name,
                    self,
                    resource_def,
                    schema,
                    mapping)
                classes[resource_name] = cls

        return classes

    def spawn(self, context={}):
        return Client(context, self.api, self.endpoint_classes)
