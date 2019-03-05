#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import copy

class ArmFile(object):
    """ An object designed to store/manage a JSON file for ARM purposes.
    """

    def __init__(self, src=None, dest=None, token=None):
        """ Constructor
        src - local file or URL to read JSON from
        dest - name of file to output
        token - base64 encoded token (user:pass) for repo auth
        """
        self.src = src
        self.dest = dest
        self.token = token
        self.__data = self.__read_json()
        self.__orig_data = self.__read_json()
        self.__changed_values = set()

    def set_src(self, src):
        """ Set src location
        """
        self.src = src

    def set_dest(self, dest):
        """ Set dest location
        """
        self.dest = dest

    def inspect(self):
        """ Print class attributes
        Helpful for debugging and informational purposes.
        """
        print(self)
        print("src: {}".format(self.src))
        print("dest: {}".format(self.dest))
        print("data: \n{}".format(json.dumps(self.__data, indent=4, sort_keys=True)))
        print("orig_data: \n{}".format(json.dumps(self.__orig_data, indent=4, sort_keys=True)))
        print("changed_values: {}".format(', '.join(self.__changed_values)))
        print("change_log: \n{}".format(json.dumps(self.get_change_log(), indent=4, sort_keys=True)))
        # print(json.dumps(self, default=lambda o: o.__dict__, indent=4, sort_keys=True))

    def __read_json(self):
        """ Read JSON from provided src location
        First attempts to read src as a local file, if that fails tries to read src as a public URL,
        if that fails tries to read src from private repo using provided token.
        """
        try:
            with open(self.src, 'r') as f:
                j = json.load(f)
            return j
        except IOError: # invalid file path
            try:
                r = requests.get(self.src, verify=False)
                return r.json()
            except json.decoder.JSONDecodeError:  # did not receive valid json
                if self.token is not None:
                    return self.__read_json_auth()
            except ValueError:  # couldn't reach URL
                raise ValueError(ArmFile.Errors.BAD_SRC_PATH)

    def __read_json_auth(self):
        """ Read JSON from URL with auth
        Reads JSON file from repo using base64 encoded auth token
        """
        try:
            headers = {
                'Authorization': "Basic {}".format(self.token),
                'Content-Type':'application/json'
            }
            r = requests.get(url=self.src, headers=headers, allow_redirects=True, verify=True)
            if r.status_code == 401:
                raise ValueError(ArmFile.Errors.BAD_AUTH)
            elif r.status_code != 200:
                raise ValueError(ArmFile.Errors.SRC_ERR)
            return r.json()
        except json.decoder.JSONDecodeError:  # did not receive valid json
            raise ValueError(ArmFile.Errors.AUTH_SRC_ERR)

    def __get_value(self, data, key, index=None):
        """ Helper method for retrieving JSON data
        Allows key to be provided in dot notation (json.parent.mykey)
        """
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
                raise KeyError(ArmFile.Errors.MISSING_KEY.format(('.').join(keys_visited)))
        if index is not None:
            return copy.deepcopy(current[index])
        else:
            return copy.deepcopy(current) # return copy so value can't be changed outside class

    def get_value(self, key, index=None):
        """ Get current value using dot notation
        """
        return self.__get_value(self.__data, key, index)

    def get_original_value(self, key, index=None):
        """ Get original value using dot notation
        """
        return self.__get_value(self.__orig_data, key, index)

    def set_value(self, key, value, index=None):
        """ Set value using dot notation
        """
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
                raise KeyError(ArmFile.Errors.MISSING_KEY.format(('.').join(keys_visited)))
        if last_key in current:
            if index is not None:
                print(current[last_key][index])
                current[last_key][index] = copy.deepcopy(value)
            else:
                current[last_key] = copy.deepcopy(value)
            self.__changed_values.add(key)
        else:
            raise KeyError(ArmFile.Errors.MISSING_KEY.format(key))

    def get_change_log(self):
        """ Show list of changes made to src data
        """
        changes = {}
        for key in self.__changed_values:
            changes[key] = {}
            changes[key]['old_value'] = self.get_original_value(key)
            changes[key]['new_value'] = self.get_value(key)
        return changes

    def write_file(self):
        """ Write JSON data to file 'dest' as JSON output
        """
        if not self.dest:
            raise ValueError(ArmFile.Errors.MISSING_DEST)
        with open(self.dest, 'w') as outfile:
            outfile.write(json.dumps(self.__data, indent=4, sort_keys=True))

    def key_exists(self, key):
        """ Check if a key exists within the JSON data
        """
        keys_list = key.split('.')
        current = self.__data
        for k in keys_list:
            try:
                current = current[k]
            except (KeyError, TypeError):
                return False
        return True

    class Errors(object):
        """ Store error messages
        """
        BAD_SRC_PATH = 'The JSON source location provided is neither a valid public URI nor a valid local file path.'
        BAD_AUTH = 'Could not authenticate with src host. Please check your authentication token.'
        SRC_ERR = 'Error while retrieving src. Please check your src URL.'
        AUTH_SRC_ERR = 'Authorized request did not receive valid JSON src.'
        MISSING_DEST = 'Missing destination path for writing file output.'
        MISSING_KEY = 'Key \'{}\' does not exist'

