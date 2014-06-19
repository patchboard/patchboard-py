# response.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import re

from exception import PatchboardError


class Response(object):

    content_pattern = re.compile(u'application/.*json')

    def __init__(self, raw):
        self.raw = raw

        self.data = None
        try:
            if Response.content_pattern.search(raw.headers[u'Content-Type']):
                self.data = raw.json()
        except KeyError:
            # If no Content-Type, don't care
            pass
        except AttributeError:
            raise PatchboardError(
                "Response has a Content-Type header but no response body")

    def __getattr__(self, name):
        try:
            return getattr(self.raw, name)
        except KeyError:
            raise AttributeError
