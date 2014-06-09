# test_discovery.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest

from patchboard import Patchboard

from patchboard.tests.fixtures import mock_pb, net_pb, pb
pytest.mark.usefixtures(mock_pb, net_pb, pb)


def test_discover(pb):
    assert isinstance(pb, Patchboard)
