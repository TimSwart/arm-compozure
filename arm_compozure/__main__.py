#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arm_file import ArmFile
from param_file import ParamFile
from template_file import TemplateFile

if __name__ == '__main__':
    # parm = ParamFile(src='tests/test_parameters.json', subscription='testSubName')
    # new_value = 'test123'
    # parm.set_parameter('storageAccountType', new_value)
    # parm.inspect()
    # parm.set_parameter('storageAccountType', '')
    # parm.inspect()
    # parm.set_parameter_as_keyvault_ref('storageAccountType', 'testsecret', 'kvrg', 'kvname')
    # parm.inspect()
    # parm = ParamFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')

    # arm = ArmFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    # # file = ArmFile('testbad.json', 'test_template')
    # arm.inspect()
    # key = 'resources'
    # my_dict = {"a": 1, "b": "string", "c": True}
    # arm.set_value(key, my_dict, 0)
    # arm.inspect()

    # arm = ArmFile(src='https://stash.kp.org/projects/AZ-INFRA/repos/arm-templates/raw/storageAccount/general/kp-azuredeploy.json?at=refs%2Fheads%2Fmaster', token='ZzU0MDY3NTpPRFUxTVRReU1EWTJORFUwT29ESXJzZ2d6SXYyRDdBcHM0STUzR1BGSkpSWQ==')
    # arm.inspect()
    # print(arm.get_value('parameters.location.defaultValue'))

    temp = TemplateFile('tests/test_template.json')
    temp.clear_tags()
    temp.inspect()
