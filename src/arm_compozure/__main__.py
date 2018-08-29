#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json_file import JsonFile

if __name__ == '__main__':
    # file = JsonFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    file = JsonFile('testbad.json', 'test_template')
    file.inspect()
