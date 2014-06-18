# trivial_example.py
#
# Copyright 2014 BitVault.
#
# Reproduces the tests in trivial_example.rb


from __future__ import print_function

import pytest
from random import randint


from patchboard.tests.fixtures import (trivial_net_pb,
                                       trivial_net_resources,
                                       trivial_net_users)
pytest.mark.usefixtures(trivial_net_pb,
                        trivial_net_resources,
                        trivial_net_users)


@pytest.mark.xfail
def test_users_create(trivial_net_users):
    user = trivial_net_users.create(
        {u'login': "foo-{0}".format(randint(1,100000))})
