#test_mapping.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest
import json

from patchboard.exception import PatchboardError

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
    assert mock_trivial_action.success_status == 201

    media_type = trivial_media_type(u"user")
    assert mock_trivial_action.headers[u"Content-Type"] == media_type
    assert mock_trivial_action.headers[u"Accept"] == media_type


class TestInputProcessing(object):

    def test_no_supplied_content(self, mock_trivial_action):
        with pytest.raises(PatchboardError):
            mock_trivial_action.process_args([])

    def test_content_objects(self, mock_trivial_action):
        content = {u'email': u'x@y.com'}
        options = mock_trivial_action.process_args([content])
        assert (isinstance(options[u'body'], str) or
                isinstance(options[u'body'], unicode))
        assert json.dumps(content) == options[u'body']
