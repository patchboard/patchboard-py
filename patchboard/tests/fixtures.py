#test_schema_manager.py
#
# Copyright 2014 BitVault.

from __future__ import print_function

#import json
import pytest

from patchboard import discover


@pytest.fixture(scope=u'class')
def pb():
    return discover(u"patchboard/api.json")


@pytest.fixture(scope=u'class')
def api(pb):
    return pb.api


@pytest.fixture(scope=u'class')
def schema_manager(pb):
    return pb.schema_manager
