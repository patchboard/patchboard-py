#test_decoration.py
#
# Copyright 2014 BitVault.
#
# Reproduces the tests in patchboard-rb's decoration_test.rb suite


from __future__ import print_function

import pytest


#from patchboard import PatchboardResources
from patchboard import Patchboard
from patchboard.mapping import Mapping

from patchboard.tests.fixtures import (trivial_spec, trivial_namespace,
                                       trivial_pb, trivial_mapping,
                                       trivial_data, trivial_repo)
pytest.mark.usefixtures(trivial_spec, trivial_namespace, trivial_pb,
                        trivial_mapping, trivial_data, trivial_repo)


# These tests don't entirely belong here
def test_pb_type(trivial_pb):
    assert isinstance(trivial_pb, Patchboard)


def test_mapping_type(trivial_mapping):
    assert isinstance(trivial_mapping, Mapping)


def test_repo_type(trivial_namespace, trivial_repo):
    namespace = trivial_namespace[u'namespace']
    assert isinstance(trivial_repo, namespace.Repository)
