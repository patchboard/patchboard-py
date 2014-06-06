# api.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

from patchboard.exception import PatchboardError


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
        # Implement!
        pass
