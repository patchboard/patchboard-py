# schema_manager.py
#
# Copyright 2014 BitVault.


# debug
# from pprint import pprint


class SchemaManager(object):

    def __init__(self, schemas):

        self.schemas = schemas
        self.id_index = {}

        for schema_source in self.schemas:
            source_id = schema_source[u'id'].rstrip(u'#')

            for name, schema in schema_source['definitions'].iteritems():
                if u'id' in schema:
                    print("has id: {0}".format(schema[u'id']))
                schema_id = schema.get(
                    u'id',
                    "{0}#{1}".format(source_id, name))

                self.index_schema(schema_id, schema)

    def index_schema(self, schema_id, schema):
        # FIXME: extensions and refs are not imported
        schema[u'id'] = schema_id
        self.id_index[schema_id] = schema

        name = schema_id.split(u'#')[1]
