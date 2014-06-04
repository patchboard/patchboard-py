#test_schema_ids.py
#
# Copyright 2014 BitVault.


from patchboard import discover


def test_ids():
    correct_schema_ids = []
    with open(u"patchboard/tests/schema_ids.txt", u"r") as file:
        for line in file:
            correct_schema_ids.append(line.rstrip())
    correct_schema_ids.sort()

    pb = discover(u"patchboard/api.json")
    schema_manager = pb.schema_manager
    schema_ids = schema_manager.id_index.keys()
    schema_ids.sort()

    assert len(correct_schema_ids) == len(schema_ids)
