#test_patchboard.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest

from patchboard import discover


@pytest.fixture()
def pb():
    return discover(u"patchboard/api.json")


def test_endpoint_classes(pb):
    with open(u"patchboard/tests/data/endpoint_classes.json", u"r") as file:
        ruby_classes = json.load(file)

    python_classes = pb.endpoint_classes

    assert len(ruby_classes) == len(python_classes)

    ruby_keys = ruby_classes.keys()
    ruby_keys.sort()

    python_keys = python_classes.keys()
    python_keys.sort()

    assert ruby_keys == python_keys

    for key in python_keys:
        assert (
            ruby_classes[key].split(u'::')[-1] ==
            python_classes[key].__name__)
