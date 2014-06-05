#test_schema_manager.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest

from patchboard import discover


@pytest.fixture()
def pb():
    return discover(u"patchboard/api.json")


@pytest.fixture()
def schema_manager(pb):
    return pb.schema_manager


def test_id_index(schema_manager):
    with open(u"patchboard/tests/data/schema_id_index.json", u"r") as file:
        correct_id_index = json.load(file)

    assert correct_id_index == schema_manager.id_index


def test_structure_equality(schema_manager):
    with open(u"patchboard/tests/data/schema_id_index.json", u"r") as file:
        correct_id_index = json.load(file)

    # Create an inequality deep in the structure to verify that '=='
    # recurses through structures when checking for equality
    id_index = schema_manager.id_index
    id_index[u'#account'][u'extends'][u'$ref'] = "foo"

    assert correct_id_index != id_index


def test_name_index(schema_manager):
    with open(u"patchboard/tests/data/schema_name_index.json", u"r") as file:
        correct_name_index = json.load(file)

    assert correct_name_index == schema_manager.name_index


def test_media_type_index(schema_manager):
    with open(u"patchboard/tests/data/schema_media_type_index.json", u"r") as file:
        correct_media_type_index = json.load(file)

    assert correct_media_type_index == schema_manager.media_type_index


def test_find(schema_manager):
    # This is almost pointless, given that the find functions are
    # trivial accessors
    with pytest.raises(KeyError):
        schema_manager.find_name(u'not a schema name')

    by_media_type = schema_manager.find_media_type(
        u'application/vnd.bitvault.transaction_signatures+json;version=1.0')

    by_id = schema_manager.find_id(by_media_type[u'id'])
    assert by_id == by_media_type

    by_name = schema_manager.find_name(by_media_type[u'id'].split(u'#')[1])
    assert by_name == by_media_type
