# resource.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import json

from exception import PatchboardError


class ResourceType(type):
    """A metaclass for resource classes."""

    # Must override to supply  default arguments
    def __new__(cls, name, patchboard, definition, schema, mapping):
        return type.__new__(cls, name, (Resource,), {})

    def __init__(cls, name, patchboard, definition, schema, mapping):
        super(ResourceType, cls).__init__(name, (Resource,), {})

        # TODO: add the singleton methods in Resource::assemble()

        #setattr(cls, 'api', lambda(self): patchboard.api)

        if schema:
            if u'properties' in schema:
                for name, schema_def in schema[u'properties'].iteritems():
                    setattr(
                        cls,
                        name,
                        lambda(self): self.attributes[name])

            if schema.get(u'additionalProperties', False) is not False:
                # FIXME: doesn't take the additional args in the ruby
                # code.
                setattr(
                    cls,
                    'method_missing',
                    lambda(self, name): self.attributes[name])

        for name, action in definition[u'actions'].iteritems():
            # FIXME: create actions

            # FIXME: implement
            setattr(cls, name, lambda(self): False)


class Resource(object):
    """Base class for resources"""

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
