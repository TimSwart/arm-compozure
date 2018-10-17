#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import copy

class ArmFile(object):
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
        print("orig_data: \n{}".format(json.dumps(self.__orig_data, indent=4, sort_keys=True)))
        print("changed_values: {}".format(', '.join(self.__changed_values)))
        print("change_log: \n{}".format(json.dumps(self.get_change_log(), indent=4, sort_keys=True)))
        # print(json.dumps(self, default=lambda o: o.__dict__, indent=4, sort_keys=True))

    def __read_json(self):
        try:
            with open(self.src, 'r') as f:
                j = json.load(f)
            return j
        except IOError: # invalid file path
            try:
                r = requests.get(self.src, verify=False)
                return r.json()
            except ValueError:  # invalid URL
                raise ValueError('The JSON source location provided is nether a valid URI nor a valid local file path.')

    def __get_value(self, data, key, index=None):
        if not key:
            return data
        keys_list = key.split('.')
        keys_visited = []
        current = data
        for k in keys_list:
            keys_visited.append(k)
            try:
                current = current[k]
            except (KeyError, TypeError):
                raise KeyError('Key \'{}\' does not exist'.format(('.').join(keys_visited)))
        if index is not None:
            return copy.deepcopy(current[index])
        else:
            return copy.deepcopy(current) # return copy so value can't be changed outside class

    def get_value(self, key, index=None):
        return self.__get_value(self.__data, key, index)

    def get_original_value(self, key, index=None):
        return self.__get_value(self.__orig_data, key, index)

    def set_value(self, key, value, index=None):
        keys_list = key.split('.')
        keys_visited = []
        last_key = keys_list[-1]
        keys_list.remove(last_key)
        current = self.__data
        for k in keys_list:
            keys_visited.append(k)
            try:
                current = current[k]
            except (KeyError, TypeError):
                raise KeyError('Key \'{}\' does not exist'.format(('.').join(keys_visited)))
        if last_key in current:
            if index is not None:
                print('test')
                print(current[last_key][index])
                current[last_key][index] = copy.deepcopy(value)
            else:
                current[last_key] = copy.deepcopy(value)
            self.__changed_values.add(key)
        else:
            raise KeyError('Key \'{}\' does not exist'.format(key))

    def get_change_log(self):
        changes = {}
        for key in self.__changed_values:
            changes[key] = {}
            changes[key]['old_value'] = self.get_original_value(key)
            changes[key]['new_value'] = self.get_value(key)
        return changes

    def write_file(self):
        if not self.dest:
            raise ValueError('Missing destination path for write')
        with open(self.dest, 'w') as outfile:
            outfile.write(json.dumps(self.__data, indent=4, sort_keys=True))

    def key_exists(self, key):
        keys_list = key.split('.')
        current = self.__data
        for k in keys_list:
            try:
                current = current[k]
            except (KeyError, TypeError):
                return False
        return True
