# api.py
#
# Copyright 2014 BitVault.


#import json


class API(object):
    """
    Interprets and represents a JSON API definition.
    """

    def __init__(self, definition):
        self.schemas = definition['schemas']
        self.mappings = definition['mappings']
        self.resources = definition['resources']

        #self.service_url = definition['service_url']
