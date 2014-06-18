# action.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import json

from exception import PatchboardError
from response import Response


class Action(object):

    def __init__(self, patchboard, name, definition):

        self.name = name
        self.patchboard = patchboard
        self.api = patchboard.api
        self.schema_manager = patchboard.schema_manager
        self.method = definition[u'method']

        self.headers = {}

        request = definition.get(u'request', None)
        response = definition.get(u'response', None)

        self.request_schema = self.response_schema = None

        if request:
            self.auth_scheme = request.get(u'authorization', None)

            content_type = request.get(u'type', None)
            if content_type:
                self.headers[u'Content-Type'] = content_type
                self.request_schema = \
                    self.schema_manager.find_media_type(content_type)

        if response and u'type' in response:

            response_type = response[u'type']
            self.headers[u'Accept'] = response_type
            self.response_schema = \
                self.schema_manager.find_media_type(response_type)

        self.success_status = response.get(u'status', 200)

    def request(self, resource, url, *args):

        options = self.prepare_request(resource, url, *args)
        # FIXME: need to finish implementing
        raw = self.patchboard.session.request(
            self.method,
            url,
            args
        )
        response = Response(raw)
        if response.status != self.success_status:
            err_msg = ("Unexpected response status: " + response.status +
                       " - " + response.body)
            raise PatchboardError(err_msg)

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
            u'headers': headers, }

        # FIXME: may not be the correct solution. I don't see where
        # context would ever aquire an 'authorizer' method in the ruby
        # code, and in any case we need to be certain of the pythonic
        # analog.
        if self.auth_scheme and u'authorizer' in context:

            credential = context[u'authorizer'](
                self.auth_scheme, resource, self.name)
            headers["Authorization"] = "{0} {1}".format(
                self.auth_scheme, credential)

        input_options = self.process_args(args)
        try:
            options[u'body'] = input_options[u'body']
        except KeyError:
            pass

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
        signature = u'.'.join([type(arg).__name__ for arg in args])
        print(args)
        print(signature)

        request_schema = None
        try:
            request_schema = self.request_schema
        except AttributeError:
            pass

        if request_schema:
            if signature == u"str" or signature == u'unicode':
                options[u'body'] = args[0]
            elif signature == u"dict" or signature == u"list":
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
