# -*- coding: utf-8 -*-
# action.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import print_function

import json

from exception import PatchboardError
from response import Response, ResponseError


class Action(object):

    def __init__(self, patchboard, name, definition):

        self.name = name
        self.patchboard = patchboard
        self.api = patchboard.api
        self.schema_manager = patchboard.schema_manager
        self.method = definition[u'method']

        # Avoid using compression
        self.headers = {u'accept-encoding': u'identity'}

        request = definition.get(u'request', None)
        response = definition.get(u'response', None)

        self.request_schema = self.response_schema = None

        if request:
            self.auth_schemes = request.get(u'authorization', [])
            if isinstance(self.auth_schemes, basestring):
                self.auth_schemes = [self.auth_schemes]

            if u'type' in request:
                self.headers[u'Content-Type'] = request[u'type']
                self.request_schema = \
                    self.schema_manager.find_media_type(request[u'type'])

        if response and u'type' in response:

            response_type = response[u'type']
            self.headers[u'Accept'] = response_type
            self.response_schema = \
                self.schema_manager.find_media_type(response_type)

        self.success_status = response.get(u'status', 200)

    def request(self, resource, url, *args):
        options = self.prepare_request(resource, url, *args)
        response = Response(self.patchboard.session.request(**options))

        if response.status_code != self.success_status:
            err_msg = ("Unexpected response status: " +
                       str(response.status_code) +
                       " - " + response.content)
            raise ResponseError(response, err_msg)

        out = self.api.decorate(resource.context,
                                self.response_schema,
                                response.data)
        out.response = response
        return out

    def prepare_request(self, resource, url, *args):

        context = resource.context
        headers = dict(self.headers)
        options = {
            u'url': url,
            u'method': self.method,
            u'headers': headers }

        input_options = self.process_args(args)

        if (hasattr(self, u'auth_schemes') and
            hasattr(context, u'authorizer') and
            callable(context.authorizer)):

            scheme, credential = context.authorizer(
                self.auth_schemes, resource, self.name, input_options)
            headers["Authorization"] = "{0} {1}".format(
                scheme, credential)

        options[u'data'] = input_options.get(u'body', None)

        # This code looks forward to the time when we have figured out
        # how we want Patchboard clients to take extra arguments for
        # requests.  Leaving it here now to show why process_args
        # returns a Hash, not just the body.
        try:
            options[u'headers'].update(input_options[u'headers'])
        except KeyError:
            pass

        return options

    def process_args(self, args):

        options = {}
        # TODO: This is weird.
        signature = u'.'.join([type(arg).__name__ for arg in args])

        request_schema = None
        try:
            request_schema = self.request_schema
        except AttributeError:
            pass

        if request_schema:
            if signature == u'str' or signature == u'unicode':
                options[u'body'] = args[0]
            elif signature == u'dict' or signature == u'list':
                options[u'body'] = json.dumps(args[0])
            else:
                raise PatchboardError(
                    u"Invalid arguments for action: request content is required"
                )
        else:
            if signature == u"":
                options[u'body'] = None
            else:
                raise PatchboardError(u"Invalid arguments for action")

        return options
