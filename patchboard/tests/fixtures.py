#test_schema_manager.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest

from patchboard import discover, Patchboard


@pytest.fixture(scope=u'class')
def pb():
    return discover(u"http://bitvault.pandastrike.com/")


@pytest.fixture(scope=u'class')
def mock_pb():
    with open(u"patchboard/api.json", u'r') as file:
        api_spec = json.load(file)

    return Patchboard(api_spec)


@pytest.fixture(scope=u'class')
def mock_api(mock_pb):
    return mock_pb.api


@pytest.fixture(scope=u'class')
def mock_schema_manager(mock_pb):
    return mock_pb.schema_manager
