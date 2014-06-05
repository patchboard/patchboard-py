# api.py
#
# Copyright 2014 BitVault.


#import json


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

        # Don't have this right now
        #self.service_url = definition['service_url']


class Mapping(object):

    def __init__(self, api, name, definition):
        self.api = api
        self.name = name
        self.definition = definition
        self.resource = definition[u"resource"]
