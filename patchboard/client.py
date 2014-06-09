# client.py
#
# Copyright 2014 BitVault.


# debug
# from pprint import pprint


from __future__ import print_function

from endpoints import Endpoints


class Client(object):

    def __init__(self, context, api, classes):
        self.context = context
        self.resources = Endpoints(context, api, classes)
