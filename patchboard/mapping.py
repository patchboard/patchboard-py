# mapping.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

from urllib import quote_plus

from exception import PatchboardError


class Mapping(object):

    def __init__(self, api, name, definition):
        self.api = api
        self.name = name
        self.definition = definition
        self.query = definition.get(u'query', None)
        self.url = definition.get(u'url', None)
        self.path = definition.get(u'path', None)
        self.template = definition.get(u'template', None)

        self.cls = None

        resource_name = definition.get(u"resource", None)
        if not resource_name:
            raise PatchboardError(u"Mapping does not specify 'resource'")

        self.resource = self.api.resources.get(resource_name, None)
        if not self.resource:
            raise PatchboardError(
                u"Mapping specifies a resource that is not defined")

        if not self.url and not self.path and not self.template:
            raise PatchboardError(
                u"Mapping is missing any form of URL specification")

    def generate_url(self, params={}):
        if self.url:
            base = self.url
        elif u'url' in params:
            base = params[u'url']
        elif self.path:
            if self.api.service_url:
                base = "{0}/{1}".format(self.api.service_url, self.path)
            else:
                raise PatchboardError(
                    u"Tried to generate url from path, but API did not define service_url")
        elif self.template:
            raise PatchboardError(
                u"Template mappings are not yet implemented in the client")

        if self.query:
            parts = []
            keys = self.query.keys()
            keys.sort()
            # TODO check query schema
            for key in keys:
                string = params.get(key, None)
                if string:
                    parts.append(
                        u"{0}={1}".format(
                            quote_plus(key),
                            quote_plus(string)))

            if len(parts) > 0:
                query_string = "?{0}".format(u'&'.join(parts))
            else:
                query_string = ""

            return base + query_string

        else:
            return base
