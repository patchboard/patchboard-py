#test_decoration.py
#
# Copyright 2014 BitVault.
#
# Reproduces the tests in patchboard-rb's decoration_test.rb suite


from __future__ import print_function

import pytest
from inspect import ismethod


import patchboard
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


# Ensure it has been injected into whatever namespace was specified
def test_repo_type(trivial_namespace, trivial_repo):
    namespace = trivial_namespace[u'namespace']
    assert isinstance(trivial_repo, namespace.Repository)


def test_action_methods(trivial_repo):
    assert ismethod(trivial_repo.get)
    assert ismethod(trivial_repo.update)
    assert ismethod(trivial_repo.delete)


def test_attr_types(trivial_repo):
    for key in [u'name', u'owner', u'refs']:
        assert trivial_repo.attributes[key]
        assert hasattr(trivial_repo, key)


def test_attr_methods(trivial_repo):
    assert(isinstance(trivial_repo.name, str) or
           isinstance(trivial_repo.name, unicode))
    assert isinstance(trivial_repo.owner, patchboard.resources.User)
    assert type(trivial_repo.refs) == dict


# FIXME: implement the rest of the decoration tests
