# -*- coding: utf-8 -*-
# patchboard.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function
from __future__ import unicode_literals
from future.utils import iteritems

import requests
import collections
import imp

from .resource import ResourceType
from .api import API
from .schema_manager import SchemaManager
from .client import Client
from .util import to_camel_case
from .exception import PatchboardError


# Default module to hold resource classes
resources = imp.new_module('resources')


def discover(url, options={}):
    """
    Retrieve the API definition from the given URL and construct
    a Patchboard to interface with it.
    """
    try:
        resp = requests.get(url, headers=Patchboard.default_headers)
    except Exception as e:
        raise PatchboardError("Problem discovering API: {0}".format(e))

    # Parse as JSON (Requests uses json.loads())
    try:
        api_spec = resp.json()
    except ValueError as e:
        raise PatchboardError("Unparseable API description: {0}".format(e))

    # Return core handle object
    return Patchboard(api_spec, options)


class Patchboard(object):
    # Provide a slightly more convenient interface than patchboard-rb:
    """
    The primary client interface to a patchboard server.

    Supported options:

        default_context:    The context used when none is specified
                            explicitly. It may either be a mapping
                            type (usually a simple dict) or a callable
                            that returns a mapping type.  The "default
                            for the default" is {}.

        resource_namespace: namespace into which  the resource classes
                            are injected.

        default_headers:    dict of HTTP headers; combined with and
                            overrides the session defaults.
    """

    default_headers = {
        'Accept': 'application/json',
        'User-Agent': 'patchboard-py v0.5.1', }

    def __init__(self, api_spec, options={}):

        self.default_headers = dict(Patchboard.default_headers,
                                    **options.get('default_headers', {}))
        # Note--resource_namespace doesn't have to be a module--it can
        # be a class or anything else that supports setattr
        self.resource_namespace = options.get('resource_namespace',
                                              resources)
        self.default_context = options.get('default_context', {})

        # Each Patchboard object is a separate session
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)

        self.api = API(api_spec)

        self.schema_manager = SchemaManager(self.api.schemas)
        self.endpoint_classes = self.create_endpoint_classes()

        # FIXME: this logic seems suspect. Why should we be saving
        # a context and resources created without the specified context?
        client = self.spawn({})
        self.context = client.context
        # Appears to be unused?
        self.resources = client.resources

    def create_endpoint_classes(self):
        classes = {}
        for resource_name, mapping in iteritems(self.api.mappings):
            schema = self.schema_manager.find_name(resource_name)
            resource_def = mapping.resource
            class_name = to_camel_case(str(resource_name))
            cls = ResourceType(class_name,
                               self,
                               resource_def,
                               schema,
                               mapping)
            mapping.cls = cls
            classes[resource_name] = cls
            setattr(self.resource_namespace, class_name, cls)

        return classes

    def spawn(self, context=None):
        """
        context may be a callable or a dict.
        """
        if context is None:
            context = self.default_context

        if isinstance(context, collections.Callable):
            context = context()

        if not isinstance(context, collections.Mapping):
            raise PatchboardError('Cannot determine a valid context')

        return Client(self, context, self.api, self.endpoint_classes)
