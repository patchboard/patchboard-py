# -*- coding: utf-8 -*-
#test_api.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest


from patchboard.tests.fixtures import (mock_pb, net_pb, mock_api, net_api, api)
pytest.mark.usefixtures(mock_pb, net_pb, mock_api, net_api, api)


def test_service_url(api):
    assert api.service_url is None


def test_resources(api):
    with open(u"patchboard/tests/data/api_resources.json", u"r") as file:
        ruby_resources = json.load(file)

    assert ruby_resources == api.resources


def test_schemas(api):
    with open(u"patchboard/tests/data/api_schemas.json", u"r") as file:
        ruby_schemas = json.load(file)

    assert ruby_schemas == api.schemas


def test_mappings(api):
    with open(u"patchboard/tests/data/api_mappings.json", u"r") as file:
        ruby_mappings = json.load(file)

    # Should really parse the value object names and compare
    ruby_keys = ruby_mappings.keys()
    ruby_keys.sort()

    python_keys = api.mappings.keys()
    python_keys.sort()

    assert ruby_keys == python_keys


def test_find_mapping(api):
    # TODO: implement!
    pass
