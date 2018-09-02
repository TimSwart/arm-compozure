#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

class JsonFile(object):
    def __init__(self, src=None, dest=None):
        self.src = src
        self.dest = dest
        self.__data = self.__read_json()

    def set_src(self, src):
        self.src = src

    def set_dest(self, dest):
        self.dest = dest

    def inspect(self):
        print(self)
        print("src: {}".format(self.src))
        print("dest: {}".format(self.dest))
        print("data: \n{}".format(json.dumps(self.__data, indent=4, sort_keys=True)))
        # print(json.dumps(self, default=lambda o: o.__dict__, indent=4, sort_keys=True))

    def __read_json(self):
        try:
            j = json.load(open(self.src))
            return j
        except IOError: # invalid file path
            try:
                r = requests.get(self.src, verify=False)
                return r.json()
            except ValueError:  # invalid URL
                raise ValueError('The JSON source location provided is nether a valid URI nor a valid local file path.')
