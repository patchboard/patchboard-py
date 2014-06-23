#test_schema_manager.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest
import imp
from collections import namedtuple
from random import randint

import patchboard.resource
from patchboard import discover, Patchboard
from patchboard.api import API
from patchboard.schema_manager import SchemaManager
from patchboard.action import Action


# A namespace to put symbols in
class PatchboardTestClass:
    pass


# Another one
PatchboardTestModule = imp.new_module(u'PatchboardTestModule')


######################################################################
# Fixtures for testing with the bitvault api
######################################################################

@pytest.fixture(scope=u'class')
def mock_pb():
    with open(u"tests/data/api.json", u'r') as file:
        api_spec = json.load(file)

    return Patchboard(api_spec)


@pytest.fixture(scope=u'class')
def net_pb():
    return discover(u"http://bitvault.pandastrike.com/")


# For tests that should run with both
@pytest.fixture(scope=u'class', params=range(0, 1))
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


def trivial_media_type(name):
    return "application/vnd.gh-knockoff.{0}+json".format(name)


@pytest.fixture(scope=u'class')
def trivial_spec():
    with open(u"tests/data/example_api.json", u'r') as file:
        api_spec = json.load(file)

    api_spec[u'service_url'] = "http://patchboard.it"
    api_spec[u'schemas'] = [api_spec.pop(u'schema')]

    return api_spec


@pytest.fixture(scope=u'class')
def trivial_api(trivial_spec):
    return API(trivial_spec)


@pytest.fixture(scope=u'class')
def trivial_schema_manager(trivial_api):
    return SchemaManager(trivial_api.schemas)


# We'll use the trivial api to test the namespace injection feature:
# test in the default, a dummy class, and a dummy module. Some code needs
# a textual name and some the namespace object, so this fixture returns
# both in pairs so they stay in sync.
@pytest.fixture(scope=u'class', params=range(0, 1))
def trivial_namespace(request):
    return [
        # Hardcode the default resource namespace
        {u'name': 'patchboard.resources', u'namespace': patchboard.resources},
        # Compute the rest of the namespaces automagically--the commented
        # line is what it currently expands to
        #{u'name': 'patchboard.tests.fixtures.PatchboardTestClass', u'namespace': PatchboardTestClass},
        {
            u'name': globals()['__name__'] + '.' + 'PatchboardTestClass',
            u'namespace': PatchboardTestClass
        },
        {
            u'name': globals()['__name__'] + '.' + 'PatchboardTestModule',
            u'namespace': PatchboardTestModule
        },
    ][request.param]


@pytest.fixture(scope=u'class')
def trivial_pb(trivial_spec, trivial_namespace):
    name = trivial_namespace[u'name']
    resource = trivial_namespace[u'namespace']
    # Not fully working yet
    #return Patchboard(trivial_spec, {u'resource_namespace': PatchboardTests})
    if name == u'patchboard.resource':
        # Test default
        return Patchboard(trivial_spec)
    else:
        return Patchboard(trivial_spec, {u'resource_namespace': resource})


@pytest.fixture(scope=u'class')
def trivial_mapping(trivial_pb):
    return trivial_pb.api.mappings[u'repository']


@pytest.fixture(scope=u'class')
def trivial_data():
    with open(u"tests/data/dectest.json", u'r') as file:
        data = json.load(file)
    return data


@pytest.fixture(scope=u'class')
def trivial_repo(trivial_mapping, trivial_data):
    return trivial_mapping.cls({}, trivial_data)


# Mocks for test_action
@pytest.fixture(scope=u'class')
def MockPB():
    return namedtuple(u'MockPB', [u'schema_manager', u'http', u'api'])


@pytest.fixture(scope=u'class')
def mock_trivial_pb(MockPB, trivial_schema_manager, trivial_api):
    return MockPB(trivial_schema_manager, None, trivial_api)


@pytest.fixture(scope=u'class')
def mock_create_action(mock_trivial_pb):
    return Action(
        mock_trivial_pb,
        u'create',
        {
            u'method': u"POST",
            u'request': {
                u'type': trivial_media_type(u"user"),
            },
            u'response': {
                u'type': trivial_media_type("user"),
                u'status': 201
            }
        })


@pytest.fixture(scope=u'class')
def MockResource():
    return namedtuple(u'MockResource', [u'context'])


@pytest.fixture(scope=u'class')
def mock_empty_get_action(mock_trivial_pb):
    return Action(
        mock_trivial_pb,
        u'get',
        {
            u'method': u"GET",
            u'response': {
                u'type': trivial_media_type("user"),
                u'status': 200
            }
        })


@pytest.fixture(scope=u'class')
def trivial_net_pb():
    return discover(u"http://localhost:1979/")


@pytest.fixture(scope=u'class')
def trivial_net_resources(trivial_net_pb):
    return trivial_net_pb.resources


@pytest.fixture(scope=u'class')
def trivial_net_users(trivial_net_resources):
    return trivial_net_resources.users


@pytest.fixture(scope=u'class')
def trivial_net_user(trivial_net_users):
    login = "foo-{0}".format(randint(1, 100000))
    return trivial_net_users.create({u'login': login})


@pytest.fixture(scope=u'class')
def trivial_net_question(trivial_net_user):
    return trivial_net_user.questions({u'category': u'Science'}).ask()
