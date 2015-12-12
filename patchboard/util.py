# -*- coding: utf-8 -*-
# util.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function
from __future__ import unicode_literals


def to_camel_case(string):
    # Transform name to CamelCase
    words = string.split('_')
    capwords = [word.capitalize() for word in words]

    return "".join(capwords)


class SchemaStruct(dict):

    def __init__(self, dict):
        # FIXME: should accept a schema and only expose the attributes
        # in the schema rather than exposing everything in the dict
        self.data = dict

    def __contains__(self, item):
        return item in self.data

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __setitem__(self, name, value):
        self.data.__setitem__(name, value)

    def __repr__(self):
        return self.data.__repr__()

class SchemaArray(list):

    def __init__(self, array):
        super(SchemaArray, self).__init__(array)
        self.response = None
