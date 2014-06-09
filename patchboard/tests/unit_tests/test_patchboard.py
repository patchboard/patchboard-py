#test_patchboard.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import pytest

from patchboard import Patchboard
from patchboard.client import Client

from patchboard.tests.fixtures import (mock_pb, net_pb, pb,
                                       mock_client, net_client, client)
pytest.mark.usefixtures(mock_pb, net_pb, pb,
                        mock_client, net_client, client)


def test_discover(pb):
    assert isinstance(pb, Patchboard)


def test_spawn(client):
    assert isinstance(client, Client)
