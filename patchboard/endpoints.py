# -*- coding: utf-8 -*-
# endpoints.py
#
# Copyright 2014 BitVault, Inc. dba Gem


# debug
# from pprint import pprint


from __future__ import print_function
from __future__ import unicode_literals
from future.utils import iteritems
from past.builtins import basestring

from types import MethodType

from .exception import PatchboardError


class Endpoints(object):

    def __init__(self, context, api, endpoint_classes):
        self.context = context
        self.api = api
        self.endpoint_classes = endpoint_classes

        for name, mapping in iteritems(self.api.mappings):
            try:
                cls = self.endpoint_classes[name]
            except KeyError:
                raise PatchboardError(
                    "No resource class for mapping '{0}'".format(name))

            if mapping.template or mapping.query:
                # A mapping with a template or query property requires
                # additional input before it can express a usable URL.  Thus
                # the endpoint method takes parameters and instantiates a
                # resource of the correct class.
                # FIXME: this implementation may not be correct

                def bind(name, cls, mapping):
                    def fn(params={}):
                        if isinstance(params, basestring):
                            url = params
                        else:
                            url = mapping.generate_url(params)
                        return cls(context, {'url': url})
                    return fn
                setattr(self, name, bind(name, cls, mapping))

            elif mapping.path:
                # When a mapping has the 'path' property, all that is needed to
                # create a usable resource is the full URL.  Thus this endpoint
                # method returns an instantiated resource directly.
                setattr(self, name, cls(context, {'url': mapping.generate_url()}))

            elif mapping.url:
                setattr(self, name, cls(context, {'url': mapping.url}))

            else:
                raise PatchboardError("Mapping '{0}' is invalid".format(name))
