#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import copy

class JsonFile(object):
    def __init__(self, src=None, dest=None):
        self.src = src
        self.dest = dest
        self.__data = self.__read_json()
        self.__orig_data = self.__read_json()
        self.__changed_values = set()

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

    def get_value(self, key):
        if not key:
            return self.__data
        keys_list = key.split('.')
        keys_visited = []
        current = self.__data
        for k in keys_list:
            keys_visited.append(k)
            try:
                current = current[k]
            except (KeyError, TypeError) as e:
                raise KeyError('Key \'{}\' does not exist'.format(('.').join(keys_visited)))
        return copy.deepcopy(current) # return copy so value can't be changed outside class

    def set_value(self, key, value):
        keys_list = key.split('.')
        keys_visited = []
        last_key = keys_list[-1]
        keys_list.remove(last_key)
        current = self.__data
        for k in keys_list:
            keys_visited.append(k)
            try:
                current = current[k]
            except (KeyError, TypeError) as e:
                raise KeyError('Key \'{}\' does not exist'.format(('.').join(keys_visited)))
        if last_key in current:
            current[last_key] = value
            self.__changed_values.add(key)
        else:
            raise KeyError('Key \'{}\' does not exist'.format(key))
