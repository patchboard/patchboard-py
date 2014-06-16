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
    mock_create_action,
    mock_empty_get_action,
    MockResource)
pytest.mark.usefixtures(
    trivial_spec,
    trivial_api,
    trivial_schema_manager,
    MockPB,
    mock_trivial_pb,
    mock_create_action,
    mock_empty_get_action,
    MockResource)


class TestWithRequestBody(object):

    def test_initialization(self, mock_create_action):
        assert mock_create_action.method == u'POST'
        assert mock_create_action.success_status == 201

        media_type = trivial_media_type(u"user")
        assert mock_create_action.headers[u"Content-Type"] == media_type
        assert mock_create_action.headers[u"Accept"] == media_type

    def test_no_supplied_content(self, mock_create_action):
        with pytest.raises(PatchboardError):
            mock_create_action.process_args([])

    def test_content_objects(self, mock_create_action):
        content = {u'email': u'x@y.com'}
        options = mock_create_action.process_args([content])
        assert (isinstance(options[u'body'], str) or
                isinstance(options[u'body'], unicode))
        assert json.dumps(content) == options[u'body']

    def test_content_strings(self, mock_create_action):
        content = {u'email': u'x@y.com'}
        content_str = json.dumps(content)
        options = mock_create_action.process_args([content_str])
        assert (isinstance(options[u'body'], str) or
                isinstance(options[u'body'], unicode))
        assert json.dumps(content) == options[u'body']

    def test_request_preparation(self, mock_create_action):
        url = u"http://api.thingy.com/"
        content = {u'email': u"x@y.com"}
        media_type = trivial_media_type(u"user")
        options = mock_create_action.prepare_request(MockResource(),
                                                     url,
                                                     content)
        assert options[u'url'] == u"http://api.thingy.com/"
        assert options[u'headers']
        assert options[u'headers'][u'Content-Type'] == media_type
        assert options[u'headers'][u'Accept'] == media_type
        assert options[u'body'] == json.dumps(content)


class TestWithoutRequestBody(object):

    def test_initialization(self, mock_empty_get_action):
        assert mock_empty_get_action.method == u'GET'
        assert mock_empty_get_action.success_status == 200

        media_type = trivial_media_type(u"user")
        assert mock_empty_get_action.headers[u"Accept"] == media_type

    def test_supplied_content(self, mock_empty_get_action):
        with pytest.raises(PatchboardError):
            mock_empty_get_action.process_args([{u'foo': u'bar'}])

    def test_no_supplied_content(self, mock_empty_get_action):
        options = mock_empty_get_action.process_args([])

        assert options[u'body'] is None
