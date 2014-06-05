#test_api.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest


from patchboard.tests.fixtures import pb, api
pytest.mark.usefixtures(pb, api)


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
