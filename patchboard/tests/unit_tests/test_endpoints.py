from __future__ import print_function
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import json
import pytest
from inspect import isfunction

from patchboard.tests.fixtures import mock_pb, net_pb, pb
pytest.mark.usefixtures(mock_pb, net_pb, pb)

def test_expected_properties(pb):
    users = pb.resources.users
    login = pb.resources.login({"email": "foo@email.com"})
    url = "http://bitvault.pandastrike.com/users?email=foo%40email.com"
    assert login.url == url

