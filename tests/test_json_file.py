#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import sys

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from src.arm_compozure.json_file import JsonFile

def test_init_check_attribute_src():
    test = JsonFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    assert hasattr(test, 'src')

def test_init_check_attribute_dest():
    test = JsonFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    assert hasattr(test, 'dest')

def test_init_check_bad_src_link_url():
    with pytest.raises(ValueError):
        JsonFile('badlink.json', 'test_template')

def test_init_check_src_link_local_file():
    JsonFile('tests/test_template.json', 'test_template')

def test_get_value_valid():
    j = JsonFile('tests/test_template.json')
    assert j.get_value('parameters.storageAccountType.defaultValue') == 'Standard_LRS'

def test_get_value_changed_outside_of_class():
    j = JsonFile('tests/test_template.json')
    v = j.get_value('parameters.storageAccountType')
    v['type'] = 'changed'
    assert v != j.get_value('parameters.storageAccountType')

def test_get_value_error():
    j = JsonFile('tests/test_template.json')
    with pytest.raises(KeyError):
        j.get_value('parameters.storageAccountType.badValue')

def test_get_value_error_2():
    j = JsonFile('tests/test_template.json')
    with pytest.raises(KeyError):
        j.get_value('parameters.storageAccountType.defaultValue.bad')
