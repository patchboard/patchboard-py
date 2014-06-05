# test_discovery.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest

from patchboard import Patchboard

from patchboard.tests.fixtures import pb
pytest.mark.usefixtures(pb)


def test_discover(pb):
    assert isinstance(pb, Patchboard)
