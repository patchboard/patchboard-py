# util.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


def to_camel_case(string):
    # Transform name to CamelCase
    words = string.split('_')
    capwords = [word.capitalize() for word in words]

    return "".join(capwords)


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

    def __getitem__(self, name):
        return self.data[name]

class SchemaArray(list):
    def __init__(self, array):
        super(list, self).__init__(array)
        self.response = None
