#test_decoration.py
#
# Copyright 2014 BitVault.
#
# Reproduces the tests in patchboard-rb's decoration_test.rb suite


from __future__ import print_function

import pytest
from inspect import ismethod


from patchboard import Patchboard
from patchboard.mapping import Mapping
from patchboard.util import SchemaStruct

from tests.fixtures import (trivial_spec, trivial_namespace,
                            trivial_pb, trivial_mapping,
                            trivial_data, trivial_repo,
                            trivial_owner, trivial_refs, trivial_tags,
                            trivial_branches)
pytest.mark.usefixtures(trivial_spec, trivial_namespace, trivial_pb,
                        trivial_mapping, trivial_data, trivial_repo,
                        trivial_owner, trivial_refs, trivial_tags,
                        trivial_branches)


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


def test_repo_attrs(trivial_repo):
    assert(isinstance(trivial_repo.name, str) or
           isinstance(trivial_repo.name, unicode))
    assert type(trivial_repo.refs) == SchemaStruct


def test_owner_type(trivial_namespace, trivial_owner):
    namespace = trivial_namespace[u'namespace']
    assert isinstance(trivial_owner, namespace.User)


def test_owner_actions(trivial_owner):
    assert ismethod(trivial_owner.get)
    assert ismethod(trivial_owner.update)


def test_owner_attributes(trivial_owner):
    attrs = trivial_owner.attributes
    assert (isinstance(attrs[u'login'], str) or
            isinstance(attrs[u'login'], unicode))
    assert (isinstance(attrs[u'email'], str) or
            isinstance(attrs[u'email'], unicode))
    assert trivial_owner.login == attrs[u'login']
    assert trivial_owner.email == attrs[u'email']


def test_repo_refs(trivial_refs):
    assert isinstance(trivial_refs, SchemaStruct)


def test_ref_tags(trivial_tags):
    assert isinstance(trivial_tags, list)
    for tag in trivial_tags:
        # FIXME: these are elements of tag.attributes in Ruby--which is
        # correct?
        assert tag[u'name']
        assert tag[u'commit']
        assert tag[u'message']


def test_branches(trivial_branches):
    print("branches type:", type(trivial_branches))
    assert isinstance(trivial_branches, SchemaStruct)
    for branch in trivial_branches.values():
        namespace = trivial_namespace[u'namespace']
        assert isinstance(branch, namespace.Branch)
        assert ismethod(trivial_branches.get)
        assert ismethod(trivial_branches.delete)
