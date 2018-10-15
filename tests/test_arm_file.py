#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import sys
import tempfile
import json
import copy

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from src.arm_compozure.arm_file import ArmFile

def test_init_check_attribute_src():
    test = ArmFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    assert hasattr(test, 'src')

def test_init_check_attribute_dest():
    test = ArmFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    assert hasattr(test, 'dest')

def test_init_check_bad_src_link_url():
    with pytest.raises(ValueError):
        ArmFile('badlink.json', 'test_template')

def test_init_check_src_link_local_file():
    ArmFile('tests/test_template.json', 'test_template')

def test_get_value_valid():
    arm = ArmFile('tests/test_template.json')
    assert arm.get_value('parameters.storageAccountType.defaultValue') == 'Standard_LRS'

def test_get_value_changed_outside_of_class():
    arm = ArmFile('tests/test_template.json')
    v = arm.get_value('parameters.storageAccountType')
    v['type'] = 'changed'
    assert v != arm.get_value('parameters.storageAccountType')

def test_get_value_error():
    arm = ArmFile('tests/test_template.json')
    with pytest.raises(KeyError):
        arm.get_value('parameters.storageAccountType.badValue')

def test_get_value_error_2():
    arm = ArmFile('tests/test_template.json')
    with pytest.raises(KeyError):
        arm.get_value('parameters.storageAccountType.defaultValue.bad')

def test_get_value_no_key():
    arm = ArmFile('tests/test_template.json')
    assert arm.get_value('') == arm._ArmFile__data

def test_get_value_list_index():
    arm = ArmFile('tests/test_template.json')
    key = 'resources'
    assert arm.get_value(key, 0) == arm._ArmFile__data[key][0]

def test_get_value_orig():
    arm = ArmFile('tests/test_template.json')
    arm.set_value('parameters.storageAccountType.defaultValue', 'changed')
    assert 'changed' == arm.get_value('parameters.storageAccountType.defaultValue')
    assert 'Standard_LRS' == arm.get_original_value('parameters.storageAccountType.defaultValue')

def test_set_value():
    arm = ArmFile('tests/test_template.json')
    arm.set_value('parameters.storageAccountType.defaultValue', 'changed')
    assert 'changed' == arm.get_value('parameters.storageAccountType.defaultValue')

def test_set_value_bad_key():
    arm = ArmFile('tests/test_template.json')
    with pytest.raises(KeyError):
        arm.set_value('parameters.storageAccountType.defaultValue.bad', 'changed')

def test_set_value_list():
    arm = ArmFile('tests/test_template.json')
    key = 'resources'
    my_list = ['a', 'b', 'c']
    arm.set_value(key, my_list)
    changes = arm.get_change_log()
    old = 'old_value'
    new = 'new_value'
    assert changes[key][old] != changes[key][new]
    assert changes[key][new] == my_list
    assert arm.get_value(key) == my_list

def test_set_value_list_index():
    arm = ArmFile('tests/test_template.json')
    key = 'resources'
    my_dict = {"a": 1, "b": "string", "c": True}
    arm.set_value(key, my_dict, 0)
    changes = arm.get_change_log()
    old = 'old_value'
    new = 'new_value'
    assert changes[key][old] != changes[key][new]
    assert changes[key][new][0] == my_dict
    assert arm.get_value(key, 0) == my_dict

def test_set_value_log_change():
    arm = ArmFile('tests/test_template.json')
    key = 'parameters.storageAccountType.defaultValue'
    arm.set_value(key, 'changed')
    assert key in arm._ArmFile__changed_values

def test_change_log():
    arm = ArmFile('tests/test_template.json')
    key = 'parameters.storageAccountType.defaultValue'
    key2 = 'parameters.location.type'
    old = 'old_value'
    new = 'new_value'
    arm.set_value(key, 'changed')
    arm.set_value(key2, 'updated')
    changes = arm.get_change_log()
    assert changes[key][old] == 'Standard_LRS'
    assert changes[key][new] == 'changed'
    assert changes[key2][old] == 'string'
    assert changes[key2][new] == 'updated'

def test_write_file():
    tmp_dir = tempfile.gettempdir()
    tmp_file = '{}/test_out.json'.format(tmp_dir)
    arm = ArmFile('tests/test_template.json', tmp_file)
    arm.write_file()
    with open(tmp_file, 'r') as f:
        j = json.load(f)
    assert j == arm._ArmFile__data
