#test_patchboard.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

import json
import pytest
from inspect import isfunction

from patchboard.tests.fixtures import pb
pytest.mark.usefixtures(pb)


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


# This doesn't work well, as too many automatic methods get mixed
# in in both languages.
# FIXME: this will also pick up data attributes on the python side.
def test_endpoint_object_methods(pb):
    with open(
            u"patchboard/tests/data/endpoint_object_methods.json", u"r") as file:
        ruby_object_methods = json.load(file)

    for key in ruby_object_methods.keys():
        ruby_object_methods[key][u'instance'] = sorted(
            ruby_object_methods[key][u'instance'])
        ruby_object_methods[key][u'class'] = sorted(
            ruby_object_methods[key][u'class'])

    python_object_methods = {}
    for clsname, cls in pb.endpoint_classes.iteritems():
        # Use dict so we don't see inherited methods
        method_list = [name for name, value in cls.__dict__.iteritems()
                       if name[0] != u'_' and isfunction(value)]
        classmethod_list = [
            name for name, value in cls.__dict__.iteritems()
            if name[0] != u'_' and type(value) == classmethod]
        python_object_methods[clsname] = {}
        python_object_methods[clsname][u'class'] = sorted(classmethod_list)
        python_object_methods[clsname][u'instance'] = sorted(method_list)

    assert ruby_object_methods == python_object_methods
