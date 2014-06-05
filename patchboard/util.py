# util.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


def to_camel_case(string):
    # Transform name to CamelCase
    words = string.split('_')
    capwords = [word.capitalize() for word in words]

    return "".join(capwords)
