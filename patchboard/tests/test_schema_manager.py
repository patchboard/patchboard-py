#test_schema_ids.py
#
# Copyright 2014 BitVault.


import json


from patchboard import discover


def test_id_index():
    with open(u"patchboard/tests/data/schema_id_index.json", u"r") as file:
        correct_id_index = json.load(file)

    pb = discover(u"patchboard/api.json")
    schema_manager = pb.schema_manager
    id_index = schema_manager.id_index

    # FIXME: someday need to verify the claim that this properly
    # recurses through the data structures to test for equality
    assert correct_id_index == id_index


def test_name_index():
    with open(u"patchboard/tests/data/schema_name_index.json", u"r") as file:
        correct_name_index = json.load(file)

    pb = discover(u"patchboard/api.json")
    schema_manager = pb.schema_manager
    name_index = schema_manager.name_index

    # FIXME: someday need to verify the claim that this properly
    # recurses through the data structures to test for equality
    assert correct_name_index == name_index


def test_media_type_index():
    with open(u"patchboard/tests/data/schema_media_type_index.json", u"r") as file:
        correct_media_type_index = json.load(file)

    pb = discover(u"patchboard/api.json")
    schema_manager = pb.schema_manager
    media_type_index = schema_manager.media_type_index

    # FIXME: someday need to verify the claim that this properly
    # recurses through the data structures to test for equality
    assert correct_media_type_index == media_type_index
