# resource.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import json

from action import Action
from exception import PatchboardError


class ResourceType(type):
    """A metaclass for resource classes."""

    # Must override to supply  default arguments
    def __new__(cls, name, patchboard, definition, schema, mapping):
        return type.__new__(cls, name, (Resource,), {})

    def __init__(cls, name, patchboard, definition, schema, mapping):

        setattr(cls, 'api', classmethod(lambda(self_): patchboard.api))

        setattr(cls, 'schema', classmethod(lambda(self_): mapping))

        if schema:
            if u'properties' in schema:
                for name, schema_def in schema[u'properties'].iteritems():
                    setattr(
                        cls,
                        name,
                        lambda(self): self.attributes[name])

            if schema.get(u'additionalProperties', False) is not False:
                # FIXME: doesn't take the block the ruby code does
                def additional_fn(self, name, *args):
                    if len(args) == 0:
                        return self.attributes[name]
                    else:
                        return super(cls, self).method_missing(name, *args)

                # FIXME: this needs to be implemented via
                # __getattr__(self, name). Possibly implemented in
                # the base class as a dict lookup with the dict
                setattr(cls, 'method_missing', additional_fn)

        setattr(
            cls,
            'generate_url',
            classmethod(
                lambda(self_, params): mapping.generate_url(params)))

        for name, action in definition[u'actions'].iteritems():
            action = Action(patchboard, name, action)

            def action_fn(self, *args):
                return action.request(self, self.url, args)

            setattr(cls, name, action_fn)

        # Must be called last
        super(ResourceType, cls).__init__(name, (Resource,), {})


class Resource(object):
    """Base class for resources"""

    @classmethod
    def decorate(cls, instance, attributes):
        # TODO: non destructive decoration
        # TODO: add some sort of validation for the input attributes.

        if cls.schema and u'properties' in cls.schema:
            context = instance.context
            properties = cls.schema[u'properties']
            for key, sub_schema in properties.iteritems():

                if key not in attributes:
                    next

                value = attributes[key]

                mapping = cls.api.find_mapping(sub_schema)
                if mapping:
                    if mapping.query:
                        # TODO: find a way to define this at runtime,
                        # not once for every instance.
                        def fn(self, params={}):
                            params[u'url'] = value[u'url']
                            url = mapping.generate_url(params)
                            return mapping.cls(context, {u'url': url})
                        setattr(instance, key, fn)
                    else:
                        attributes[key] = mapping.cls(context, value)
                else:
                    attributes[key] = cls.api.decorate(
                        context,
                        sub_schema,
                        value)

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
