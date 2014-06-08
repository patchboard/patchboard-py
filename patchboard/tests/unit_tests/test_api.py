#test_api.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest


from patchboard.tests.fixtures import mock_pb, mock_api
pytest.mark.usefixtures(mock_pb, mock_api)


def test_service_url(mock_api):
    assert mock_api.service_url is None


def test_resources(mock_api):
    with open(u"patchboard/tests/data/api_resources.json", u"r") as file:
        ruby_resources = json.load(file)

    assert ruby_resources == mock_api.resources


def test_schemas(mock_api):
    with open(u"patchboard/tests/data/api_schemas.json", u"r") as file:
        ruby_schemas = json.load(file)

    assert ruby_schemas == mock_api.schemas


def test_mappings(mock_api):
    with open(u"patchboard/tests/data/api_mappings.json", u"r") as file:
        ruby_mappings = json.load(file)

    # Should really parse the value object names and compare
    ruby_keys = ruby_mappings.keys()
    ruby_keys.sort()

    python_keys = mock_api.mappings.keys()
    python_keys.sort()

    assert ruby_keys == python_keys


def test_find_mapping(mock_api):
    # TODO: implement!
    pass
