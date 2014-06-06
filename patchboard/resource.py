# resource.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import json

from exception import PatchboardError


class ResourceType(type):
    """A metaclass for resource classes."""

    # Must override to supply  default arguments
    def __new__(cls, name):
        return type.__new__(cls, name, (Resource,), {})

    def __init__(cls, name):
        super(ResourceType, cls).__init__(name, (Resource,), {})

        # Test method
        def foo(self):
            print("Foo!\n")
        setattr(cls, 'foo', foo)

        # TODO: add the rest of the methods


class Resource(object):

    @classmethod
    def decorate(cls, instance, attributes):
        # TODO: implement! Or use a different system...
        return attributes

    def __init__(self, context, attributes={}):
        self.context = context
        self.attributes = Resource.decorate(self, attributes)
        self.url = self.attributes[u'url']

    # TODO: implement
    #def __str__(self):

    def __len__(self):
        return len(self.attributes)

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    #def __delitem__(self, key):
    #    del self.attributes[key]

    def __contains__(self, obj):
        return (obj in self.attributes)

    def curl(self):
        raise PatchboardError(u"Resource.curl() not implemented")

    def to_hash(self):
        return self.attributes

    def to_json(self):
        return json.generate(self.attributes)
