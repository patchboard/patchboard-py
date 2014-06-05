# test_discovery.py
#
# Copyright 2014 BitVault.


from __future__ import print_function


from patchboard import discover, Patchboard


def test_discover():
    assert isinstance(discover(u"patchboard/api.json"), Patchboard)
