# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem


# debug
# from pprint import pprint


from __future__ import print_function
from __future__ import unicode_literals

from .endpoints import Endpoints


class Client(object):

    def __init__(self, main_pb, context, api, classes):
        self.main_pb = main_pb
        self.context = context
        self.resources = Endpoints(context, api, classes)

    def spawn(self, context=None):
        return self.main_pb.spawn(context)
