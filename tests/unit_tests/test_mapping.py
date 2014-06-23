#test_mapping.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest


from patchboard.exception import PatchboardError
from tests.fixtures import (mock_pb, net_pb, mock_api, net_api, api)
pytest.mark.usefixtures(mock_pb, net_pb, mock_api, net_api, api)


def test_generate_url(api):
    with open(u"tests/data/api_mappings_urls.json", u"r") as file:
        ruby_urls = json.load(file)

    python_urls = {}
    for key, mapping in api.mappings.iteritems():
        try:
            #print(len(mapping.generate_url()))
            python_urls[key] = mapping.generate_url()
        except PatchboardError as e:
            python_urls[key] = "Exception: '{0}'".format(e)

    assert ruby_urls == python_urls
