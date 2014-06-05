# schema_manager.py
#
# Copyright 2014 BitVault.


# debug
# from pprint import pprint


from __future__ import print_function


class SchemaManager(object):

    def __init__(self, schemas):

        self.schemas = schemas
        self.id_index = {}
        self.name_index = {}
        self.media_type_index = {}

        for schema_source in self.schemas:
            source_id = schema_source[u'id'].rstrip(u'#')

            for name, schema in schema_source['definitions'].iteritems():

                self.index_schema(source_id, name, schema)

    def index_schema(self, source_id, name, schema):
        # FIXME: extensions and refs are not imported

        # Create id if it doesn't already exist
        schema_id = schema.setdefault(
            u'id', "{0}#{1}".format(source_id, name))

        # Add to id index
        self.id_index[schema_id] = schema

        # Add to name index
        self.name_index[name] = schema

        # If we have a specified media type, add to that index
        media_type = schema.get(u'mediaType', False)
        if media_type:
            self.media_type_index[media_type] = schema

    # On lookup failures let KeyError propagate to the caller

    def find_media_type(self, media_type):
        return self.media_type_index[media_type]

    def find_name(self, name):
        return self.name_index[name]

    def find_id(self, schema_id):
        return self.id_index[schema_id]
