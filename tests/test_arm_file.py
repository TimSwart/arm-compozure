#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import sys

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
    j = ArmFile('tests/test_template.json')
    assert j.get_value('parameters.storageAccountType.defaultValue') == 'Standard_LRS'

def test_get_value_changed_outside_of_class():
    j = ArmFile('tests/test_template.json')
    v = j.get_value('parameters.storageAccountType')
    v['type'] = 'changed'
    assert v != j.get_value('parameters.storageAccountType')

def test_get_value_error():
    j = ArmFile('tests/test_template.json')
    with pytest.raises(KeyError):
        j.get_value('parameters.storageAccountType.badValue')

def test_get_value_error_2():
    j = ArmFile('tests/test_template.json')
    with pytest.raises(KeyError):
        j.get_value('parameters.storageAccountType.defaultValue.bad')

def test_get_value_no_key():
    j = ArmFile('tests/test_template.json')
    assert j.get_value('') == j._ArmFile__data

def test_set_value():
    j = ArmFile('tests/test_template.json')
    j.set_value('parameters.storageAccountType.defaultValue', 'changed')
    assert 'changed' == j.get_value('parameters.storageAccountType.defaultValue')

def test_set_value_bad_key():
    j = ArmFile('tests/test_template.json')
    with pytest.raises(KeyError):
        j.set_value('parameters.storageAccountType.defaultValue.bad', 'changed')

def test_set_value_log_change():
    j = ArmFile('tests/test_template.json')
    key = 'parameters.storageAccountType.defaultValue'
    j.set_value(key, 'changed')
    assert key in j._ArmFile__changed_values

def test():
    j = ArmFile('tests/test_template.json')
    key = 'parameters.storageAccountType.defaultValue'
    key2 = 'parameters.location.type'
    old = 'old_value'
    new = 'new_value'
    j.set_value(key, 'changed')
    j.set_value(key2, 'updated')
    changes = j.get_change_log()
    assert changes[key][old] == 'Standard_LRS'
    assert changes[key][new] == 'changed'
    assert changes[key2][old] == 'string'
    assert changes[key2][new] == 'updated'
