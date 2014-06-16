#test_mapping.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest

from patchboard.tests.fixtures import (
    trivial_media_type,
    trivial_spec,
    trivial_api,
    trivial_schema_manager,
    MockPB,
    mock_trivial_pb,
    mock_trivial_action)
pytest.mark.usefixtures(
    trivial_spec,
    trivial_api,
    trivial_schema_manager,
    MockPB,
    mock_trivial_pb,
    mock_trivial_action)


def test_initialization(mock_trivial_action):
    assert mock_trivial_action.method == u'POST'
    assert mock_trivial_action.status == 201

    media_type = trivial_media_type(u"user")
    assert mock_trivial_action.headers[u"Content-Type"] == media_type
    assert mock_trivial_action.headers[u"Accept"] == media_type
