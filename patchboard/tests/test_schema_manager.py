#test_schema_ids.py
#
# Copyright 2014 BitVault.


import json


from patchboard import discover


def test_ids():
    with open(u"patchboard/tests/schema_id_index.json", u"r") as file:
        correct_schema_id_index = json.load(file)

    pb = discover(u"patchboard/api.json")
    schema_manager = pb.schema_manager
    schema_id_index = schema_manager.id_index

    # FIXME: someday need to verify the claim that this properly
    # recurses through the data structures to test for equality
    assert correct_schema_id_index == schema_id_index
