#test_schema_manager.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest

from patchboard import discover, Patchboard
from patchboard.api import API
from patchboard.schema_manager import SchemaManager


def media_type(name):
    return "application/vnd.gh-knockoff.{0}+json".format(name)


######################################################################
# Fixtures for testing with the bitvault api
######################################################################

@pytest.fixture(scope=u'class')
def mock_pb():
    with open(u"patchboard/tests/data/api.json", u'r') as file:
        api_spec = json.load(file)

    return Patchboard(api_spec)


@pytest.fixture(scope=u'class')
def net_pb():
    return discover(u"http://bitvault.pandastrike.com/")


# For tests that should run with both
@pytest.fixture(scope=u'class', params=range(0, 2))
def pb(request, mock_pb, net_pb):
    return [mock_pb, net_pb][request.param]


@pytest.fixture(scope=u'class')
def mock_client(mock_pb):
    return mock_pb.spawn()


@pytest.fixture(scope=u'class')
def net_client(net_pb):
    return net_pb.spawn()


# For tests that should run with both
@pytest.fixture(scope=u'class', params=range(0, 2))
def client(request, mock_client, net_client):
    return [mock_client, net_client][request.param]


@pytest.fixture(scope=u'class')
def mock_api(mock_pb):
    return mock_pb.api


@pytest.fixture(scope=u'class')
def net_api(net_pb):
    return net_pb.api


# For tests that should run with both
@pytest.fixture(scope=u'class', params=range(0, 2))
def api(request, mock_api, net_api):
    return [mock_api, net_api][request.param]


@pytest.fixture(scope=u'class')
def mock_schema_manager(mock_pb):
    return mock_pb.schema_manager


@pytest.fixture(scope=u'class')
def net_schema_manager(net_pb):
    return net_pb.schema_manager


@pytest.fixture(scope=u'class', params=range(0, 2))
def schema_manager(request, mock_schema_manager, net_schema_manager):
    return [mock_schema_manager, net_schema_manager][request.param]

######################################################################
# Fixtures for testing with the trivial api
######################################################################


@pytest.fixture(scope=u'class')
def trivial_spec():
    with open(u"patchboard/tests/data/trivial_api.json", u'r') as file:
        api_spec = json.load(file)

    api_spec[u'schemas'] = [api_spec.pop(u'schema')]

    return api_spec


@pytest.fixture(scope=u'class')
def trivial_api(trivial_spec):
    return API(trivial_spec)


@pytest.fixture(scope=u'class')
def trivial_schema_manager(trivial_api):
    return SchemaManager(trivial_api.schemas)


#@pytest.fixture(scope=u'class')
#def trivial_pb(trivial_spec):
#    return Patchboard(trivial_spec)
