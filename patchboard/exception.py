# exception.py
#
# Copyright 2014 BitVault.
#
# Exceptions for patchboard-py
#
# TODO: should create individual exception classes as needed so clients
# can write more useful except clauses.


from __future__ import print_function


class PatchboardError(RuntimeError):
    pass
