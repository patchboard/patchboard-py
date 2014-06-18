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
    #pp(users)
    #pp(pb.resources.login)
    login = pb.resources.login
    login({"email": "foo@email.com"})

