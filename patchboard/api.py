# -*- coding: utf-8 -*-
# api.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function
from __future__ import unicode_literals
from future.utils import iteritems

from .mapping import Mapping
from .util import SchemaStruct, SchemaArray


class API(object):
    """
    Interprets and represents a JSON API definition.
    """

    def __init__(self, definition):

        self.service_url = definition.get('service_url', None)

        # Handle resources
        self.resources = definition['resources']
        for name, value in iteritems(self.resources):
            value['name'] = name

        # Handle schemas
        # FIXME: test that schemas is really an array
        self.schemas = definition['schemas']

        # Handle mappings
        self.mappings = {}
        for name, mapping in iteritems(definition['mappings']):
            self.mappings[name] = Mapping(self, name, mapping)

    def find_mapping(self, schema):
        id = schema.get('id', None) or schema.get('$ref', None)
        if id:
            name = id.split('#')[-1]
            return self.mappings.get(name, None)
        else:
            return None

    def decorate(self, context, schema, data):
        if not schema:
            return SchemaStruct(data)

        mapping = self.find_mapping(schema)
        if mapping:
            # when we have a resource class, instantiate it using the
            # input data.
            data = mapping.cls(context, data)
        else:
            # Otherwise traverse the schema in search of subschemas
            # that have resource classes available.

            items = schema.get('items', None)
            if items:
                # TODO: handle the case where schema.items is an array,
                # which signifies a tuple.  schema.additionalItems
                # then becomes important.
                data = [self.decorate(context, items, item)
                        for item in data]
                data = SchemaArray(data)

            properties = schema.get('properties', None)
            if properties:
                for key, prop_schema in iteritems(properties):
                    value = data.get(key, None)
                    if value:
                        data[key] = self.decorate(
                            context,
                            prop_schema,
                            value)

            additionalProperties = schema.get('additionalProperties', None)
            if additionalProperties:
                for key, value in iteritems(data):
                    if ('properties' not in schema or
                            key not in schema['properties']):
                        data[key] = self.decorate(
                            context,
                            schema['additionalProperties'],
                            value)



            if isinstance(data, dict):
                data = SchemaStruct(data)

        return data
