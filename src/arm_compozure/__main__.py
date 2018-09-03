#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arm_file import ArmFile

if __name__ == '__main__':
    file = ArmFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    # file = ArmFile('testbad.json', 'test_template')
    file.inspect()
