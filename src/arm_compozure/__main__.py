#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arm_file import ArmFile
from param_file import ParamFile

if __name__ == '__main__':
    parm = ParamFile('tests/test_parameters.json')
    new_value = 'test123'
    parm.set_parameter('storageAccountType', new_value)
    parm.inspect()
    # parm = ParamFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')

    # arm = ArmFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    # # file = ArmFile('testbad.json', 'test_template')
    # arm.inspect()
    # key = 'resources'
    # my_dict = {"a": 1, "b": "string", "c": True}
    # arm.set_value(key, my_dict, 0)
    # arm.inspect()
