# -*- coding: utf-8 -*-
# headers.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function

import re

class Headers(object):
    # matches the form some="thing", some=thing
    # FIXME: also matches some="thing
    WWWAuthRegex = re.compile(r'([^\s,]+)="?(^\s,"]+)"?')

    def parse_www_auth(string):
        parsed = {}
        # FIXME:  This assumes that no quoted strings have spaces within.
        tokens = string.split(" ")
        name = tokens.pop()
        parsed[name] = {}
        for token in tokens:
            # Now I have two problems
            match = self.WWWAuthRegex.match(token)
            if match:
                parsed[name][match.group(1)] = group(2)
            else:
                name = token
                parsed[name] = {}
        return parsed

