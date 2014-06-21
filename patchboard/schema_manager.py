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

            # TODO: Is this test necessary?
            if u'definitions' in schema_source:
                for name, schema in schema_source[u'definitions'].iteritems():
                    self.index_schema(source_id, name, schema)

    def index_schema(self, source_id, name, schema):
        # FIXME: extensions and refs are not imported

        # Create id if it doesn't already exist
        schema_id = schema.setdefault(
            u'id', u"{0}#{1}".format(source_id, name))

        # Add to id index
        self.id_index[schema_id] = schema

        # Add to name index
        self.name_index[name] = schema

        # If we have a specified media type, add to that index
        media_type = schema.get(u'mediaType', False)
        if media_type:
            self.media_type_index[media_type] = schema

    # TODO: consider making these properties so the usual dict
    # methods can be used.
    def find_media_type(self, media_type, default=None):
        return self._find(self.media_type_index, media_type, default)

    def find_name(self, name, default=None):
        return self._find(self.name_index, name, default)

    def find_id(self, schema_id, default=None):
        return self._find(self.id_index, schema_id, default)

    def _find(self, index, key, default=None):
        return index.get(key, default)
