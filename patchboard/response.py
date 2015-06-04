# -*- coding: utf-8 -*-
# response.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function
from __future__ import unicode_literals
from future.utils import iteritems

import re

from .exception import PatchboardError
from .headers import Headers

class Response(object):

    content_pattern = re.compile('application/.*json')

    def __init__(self, raw):
        self.raw = raw
        self.data = None
        try:
            if Response.content_pattern.search(raw.headers['Content-Type']):
                self.data = raw.json()
        except KeyError:
            # If no Content-Type, don't care
            pass
        except AttributeError:
            raise PatchboardError(
                "Response has a Content-Type header but no response body")

        self.parsed_headers = self.parse_headers()

    def __getattr__(self, name):
        try:
            return getattr(self.raw, name)
        except KeyError:
            raise AttributeError

    def parse_headers(self):
        headers = {}
        for (key, value) in iteritems(self.raw.headers):
            if 'www-authenticate' in key:
                headers['WWW-Authenticate'] = Headers.parse_www_auth(value)
            else:
                headers[key] = value
        return headers

class ResponseError(PatchboardError):
    def __init__(self, response, message):
        self.response = response
        self.headers = response.parse_headers()
        self.status_code = response.status_code
        self.response = response
        self.message = message

    def __str__(self):
        return self.message
