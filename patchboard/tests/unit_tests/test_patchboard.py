#test_patchboard.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import pytest
import json

from patchboard import Patchboard
from patchboard.client import Client
from patchboard.endpoints import Endpoints

from patchboard.tests.fixtures import (mock_pb, net_pb, pb,
                                       mock_client, net_client, client)
pytest.mark.usefixtures(mock_pb, net_pb, pb,
                        mock_client, net_client, client)


def test_discover(pb):
    assert isinstance(pb, Patchboard)


def test_spawn_missing(pb, client):

    # Does it work with an empty context?
    assert isinstance(client, Client)


def test_spawn_empty(pb):
    assert isinstance(pb.spawn({}), Client)


def test_spawn_creator():

    # Does it work with a context creator?
    def context_creator():
        return {}

    with open(u"patchboard/tests/data/api.json", u'r') as file:
        api_spec = json.load(file)

    pb = Patchboard(api_spec, options={u'context_creator':
                                       context_creator})
    assert isinstance(pb.spawn(), Client)


def test_client(client):
    assert isinstance(client.resources, Endpoints)
