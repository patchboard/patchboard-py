# -*- coding: utf-8 -*-
# headers.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function
from __future__ import unicode_literals

import re

class Headers(object):
    # matches the form some="thing", some=thing
    # FIXME: also matches some="thing
    WWWAuthRegex = re.compile(r'([^\s,]+)="?([^\s,"]+)"?')

    @classmethod
    def parse_www_auth(cls, string):
        arrays = []
        current = None
        tokens = string.split(" ")
        for token in tokens:
            if "=" in token:
                current.append(token)
            else:
                current = [token]
                arrays.append(current)


        challenges = {}
        for challenge in arrays:
            name = challenge[0]
            pairs = challenge[1:]
            if len(pairs) == 0:
                raise Exception("Invalid WWW-Authenticate header: {}".format(string) )

            challenges[name] = {}

            for pair in pairs:
                match = cls.WWWAuthRegex.match(pair)
                if match:
                    challenges[name][match.group(1)] = match.group(2)
                else:
                    raise Exception("Invalid WWW-Authenticate header: {}".format(string) )

        return challenges
