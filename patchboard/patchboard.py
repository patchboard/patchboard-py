# patchboard.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import requests
import collections
import imp

from resource import ResourceType
from api import API
from schema_manager import SchemaManager
from client import Client
from util import to_camel_case
from exception import PatchboardError


# Default module to hold resource classes
resources = imp.new_module(u'resources')


def discover(url, options={}):
    """
    Retrieve the API definition from the given URL and construct
    a Patchboard to interface with it.
    """
    # Retrieve API definition from server
    try:
        resp = requests.get(url, headers=Patchboard.default_headers)
    except Exception as e:
        raise PatchboardError("Problem discovering API: {0}".format(e))

    # Parse as JSON
    try:
        # Using the built-in requests json parser--find out if it
        # is different code than the json package, if so we may have
        # consistency issues.
        api_spec = resp.json()
    except Exception as e:
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

        resource_namespace: namespace in which to inject the resource
                            classes.

        default_headers:    dict of HTTP headers; combined with and
                            overrides the session defaults.
    """

    default_headers = {
        u'Accept': u'application/json',
        u'User-Agent': u'patchboard-py v0.1.0', }

    def __init__(self, api_spec, options={}):

        self.default_headers = options.get(u'default_headers', None)
        # Note--resource_namespace doesn't have to be a module--it can
        # be a class or anything else that supports setattr
        self.resource_namespace = options.get(
            u'resource_namespace',
            resources)
        self.default_context = options.get(u'default_context', {})

        # Each Patchboard object is a separate session
        self.session = requests.Session()
        self.session.headers.update(Patchboard.default_headers)
        if self.default_headers:
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
        for resource_name, mapping in self.api.mappings.iteritems():
            schema = self.schema_manager.find_name(resource_name)
            resource_def = mapping.resource
            class_name = to_camel_case(str(resource_name))
            cls = ResourceType(
                class_name,
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
            raise PatchboardError(u'Cannot determine a valid context')

        return Client(context, self.api, self.endpoint_classes)
