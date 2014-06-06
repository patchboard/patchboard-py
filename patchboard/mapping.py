# api.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


class Mapping(object):

    def __init__(self, api, name, definition):
        self.api = api
        self.name = name
        self.definition = definition
        self.resource = definition[u"resource"]
