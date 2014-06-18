# response.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import json
import re


class Response(object):

    content_pattern = re.compile(u'application/.*json')

    def __init__(self, raw):
        self.raw = raw

        self.data = None
        try:
            if Response.content_pattern.search(raw.headers[u'Content-Type']):
                self.data = json.load(raw.body)
        except KeyError:
            pass

    def __getattr__(self, name):
        try:
            return getattr(self.raw, name)
        except KeyError:
            raise AttributeError
