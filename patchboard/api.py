# api.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

from mapping import Mapping


class SchemaStruct(object):

    def __init__(self, output_struct):
        # FIXME: should accept a schema and only expose the attributes
        # in the schema rather than exposing everything in the dict
        self.data = output_struct

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError


class SchemaArray(list):
    def __init__(self, array):
        super(list, self).__init__(array)
        self.response = None


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

    def find_mapping(self, schema):
        id = schema.get(u'id', None) or schema.get(u'$ref', None)
        if id:
            name = id.split(u'#')[-1]
            return self.mappings.get(name, None)
        else:
            return None

    def decorate(self, context, schema, data):
        if not schema:
            return data

        mapping = self.find_mapping(schema)
        if mapping:
            # when we have a resource class, instantiate it using the
            # input data.
            data = mapping.cls(context, data)
        else:
            # Otherwise traverse the schema in search of subschemas
            # that have resource classes available.
            schema_type = schema[u'type']
            if schema_type == u'array':
                # TODO: handle the case where schema.items is an array,
                # which signifies a tuple.  schema.additionalItems
                # then becomes important.
                data = [self.decorate(context, schema[u'items'], item)
                        for item in data]
                data = SchemaArray(data)

            elif schema_type == u'object':
                if u'properties' in schema:
                    for key, prop_schema in schema[u'properties'].iteritems():
                        value = data.get(key, None)
                        if value:
                            data[key] = self.decorate(
                                context,
                                prop_schema,
                                value)

                # TODO: handle schema.patternProperties
                # TODO: consider alternative to iterating over all keys.
                if u'additionalProperties' in schema:
                    for key, value in data:
                        if (u'properties' not in schema or
                                key not in schema[u'properties']):
                            data[key] = self.decorate(
                                context,
                                schema[u'additionalProperties'],
                                value)

                data = SchemaStruct(data)

        return data
