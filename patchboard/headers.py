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
        arrays = []
        current = None

        tokens = string.split(" ")

        for token in tokens:
            if "=" in token:
                current.append(token)
            else:
                current = [token]
                arrays.push(current)


        challenges = {}
        for challenge in arrays:
            name, challege[0]
            pairs = challenge[1:]
            if pairs.length == 0:
                raise Exception("Invalid WWW-Authenticate header")

            challenges[name] = {}

            for pair in pairs:
                match = self.WWWAuthRegex.match(pair)
                if match:
                    challenges[name][match.group(1)] = group(2)
                else:
                    raise Exception("Invalid WWW-Authenticate header")

        return challenges

