# -*- coding: utf-8 -*-
# resource.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function
from __future__ import unicode_literals
from future.utils import iteritems

import json

from .action import Action
from .exception import PatchboardError


class ResourceType(type):
    """A metaclass for resource classes."""

    # Must override to supply  default arguments
    def __new__(cls, name, patchboard, definition, schema, mapping):
        return type.__new__(cls, str(name), (Resource,), {})

    def __init__(cls, name, patchboard, definition, schema, mapping):

        setattr(cls, 'api', patchboard.api)

        setattr(cls, 'schema', schema)

        setattr(cls, 'mapping', mapping)

        if schema:
            if 'properties' in schema:
                for name, schema_def in iteritems(schema['properties']):

                    property_mapping = cls.api.find_mapping(schema_def)
                    if property_mapping:
                        if property_mapping.query:
                            # FIXME: Put in a separate method here and
                            # elsewhere
                            def bind_property_query(name, property_mapping):
                                def fn(self, params={}):
                                    params['url'] = self.attributes[name]['url']
                                    url = property_mapping.generate_url(params)
                                    return property_mapping.cls(self.context,
                                                                {'url': url})
                                return fn
                            setattr(cls, name, bind_property_query(
                                name,
                                property_mapping))
                        else:
                            def bind_property_mapping(name, property_mapping):
                                def fn(self):
                                    return property_mapping.cls(
                                        self.context,
                                        self.attributes[name])
                                return fn
                            setattr(cls, name, property(bind_property_mapping(
                                name,
                                property_mapping)))
                    else:
                        def bind_property_nomapping(name):
                            def fn(self):
                                return self.attributes[name] if name in self.attributes else None
                            return fn
                        setattr(cls, name, property(bind_property_nomapping(name)))

            # The 'is not False' only matters if additionalProperties is
            # None, basically--are these semantics critical?
            if schema.get('additionalProperties', False) is not False:
                def additional_fn(self, name):
                    # TODO: this may not be the correct semantics--
                    # in python we don't have access to the arguments and
                    # so can't condition the return value on them as the ruby
                    # code does. If we need that, just have __getattr__
                    # return a method_missing method that does what the Ruby
                    # code does.
                    try:
                        return self.attributes[name]
                    except KeyError:
                        raise AttributeError

                setattr(cls, '__getattr__', additional_fn)

        setattr(
            cls,
            'generate_url',
            classmethod(lambda self_, params: mapping.generate_url(params)))

        if definition:
            actions = definition.get('actions', {})
            for name, action in iteritems(actions):
                action = Action(patchboard, name, action)

                def bind_action(action):
                    def action_fn(self, *args):
                        return action.request(self, self.url, *args)
                    return action_fn

                setattr(cls, name, bind_action(action))

        # Must be called last
        super(ResourceType, cls).__init__(name, (Resource,), {})


class Resource(object):
    """Base class for resources"""

    @classmethod
    def decorate(cls, instance, attributes):
        # TODO: non destructive decoration
        # TODO: add some sort of validation for the input attributes

        class_schema = getattr(cls, 'schema', None)
        if class_schema:
            properties = class_schema.get('properties', None)
            if properties:
                for key, sub_schema in iteritems(properties):
                    value = attributes.get(key, None)
                    mapping = cls.api.find_mapping(sub_schema)
                    if value and not mapping:
                        attributes[key] = cls.api.decorate(instance.context,
                                                           sub_schema,
                                                           value)

        return attributes

    def __init__(self, context, attributes={}):
        self.context = context
        self.attributes = self.decorate(self, attributes)
        self.url = self.attributes.get('url', None)

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
        raise PatchboardError("Resource.curl() not implemented")

    def to_hash(self):
        return self.attributes

    def to_json(self):
        return json.dumps(self.attributes)
