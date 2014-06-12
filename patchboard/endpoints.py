# endpoints.py
#
# Copyright 2014 BitVault.


# debug
# from pprint import pprint


from __future__ import print_function

from types import MethodType

from exception import PatchboardError


class Endpoints(object):

    def __init__(self, context, api, endpoint_classes):
        self.context = context
        self.api = api
        self.endpoint_classes = endpoint_classes

        for name, mapping in self.api.mappings.iteritems():
            try:
                cls = self.endpoint_classes[name]
            except KeyError:
                raise PatchboardError(
                    u"No resource class for mapping '{0}'".format(name))

            if mapping.template or mapping.query:
                # A mapping with a template or query property requires
                # additional input before it can express a usable URL.  Thus
                # the endpoint method takes parameters and instantiates a
                # resource of the correct class.
                # FIXME: this implementation may not be correct
                def fn(self, params={}):
                    if isinstance(params, str):
                        url = params
                    else:
                        url = mapping.generate_url(params)
                    return cls(context, {u'url': url})

                endpoint = MethodType(fn, self, type(self))

            elif mapping.path:
                # When a mapping has the 'path' property, all that is needed to
                # create a usable resource is the full URL.  Thus this endpoint
                # method returns an instantiated resource directly.
                endpoint = cls(context, {u'url': mapping.generate_url()})

            elif mapping.url:
                endpoint = cls(context, {u'url': mapping.url})

            else:
                raise PatchboardError(u"Mapping '{0}' is invalid".format(name))

            setattr(self, name, endpoint)
