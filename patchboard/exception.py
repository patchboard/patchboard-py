# -*- coding: utf-8 -*-
# exception.py
#
# Copyright 2014 BitVault, Inc. dba Gem
#
# Exceptions for patchboard-py
#
# TODO: should create individual exception classes as needed so clients
# can write more useful except clauses.


from __future__ import print_function
from __future__ import unicode_literals


class PatchboardError(RuntimeError):
    pass
