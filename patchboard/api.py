# api.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

from mapping import Mapping


class API(object):
    """
    Interprets and represents a JSON API definition.
    """

    def __init__(self, definition):

        self.service_url = definition.get(u'service_url', None)

        # Handle resources
        self.resources = definition['resources']
        for name, value in self.resources.iteritems():
            value[u'name'] = name

        # Handle schemas
        # FIXME: test that schemas is really an array
        self.schemas = definition['schemas']

        # Handle mappings
        self.mappings = {}
        for name, mapping in definition['mappings'].iteritems():
            self.mappings[name] = Mapping(self, name, mapping)

    def find_mapping(schema):
        # TODO: implement!
        pass

    def decorate(context, schema, data):
        # TODO: implement!
        pass
