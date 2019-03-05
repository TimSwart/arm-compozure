#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import config
from arm_compozure.param_file import ParamFile

def test_init():
    test = ParamFile('https://raw.githubusercontent.com/TimSwart/azure-quickstart-templates/master/101-storage-account-create/azuredeploy.json', 'test_template')
    assert hasattr(test, 'src')
    assert test.get_value('parameters.storageAccountType.defaultValue') == 'Standard_LRS'

def test_get_parameter_base_case():
    parm = ParamFile('tests/test_parameters.json')
    assert parm.get_parameter('storageAccountType') == "Standard_GRS"

def test_get_parameter_invalid_key():
    with pytest.raises(KeyError):
        parm = ParamFile('tests/test_parameters.json')
        parm.get_parameter('badParamName')

def test_get_parameter_key_vault_ref():
    parm = ParamFile('tests/test_parameters.json')
    expected = {
        "reference": {
            "keyVault": {
                "id": "/subscriptions/<subscription-id>/resourceGroups/examplegroup/providers/Microsoft.KeyVault/vaults/<vault-name>"
            },
            "secretName": "examplesecret"
        }
    }
    assert parm.get_parameter('adminPassword') == expected

def test_set_parameter_base_case():
    parm = ParamFile('tests/test_parameters.json')
    new_value = 'test123'
    parm.set_parameter('storageAccountType', new_value)
    assert parm.get_parameter('storageAccountType') == new_value

def test_set_parameter_invalid_key():
    with pytest.raises(KeyError):
        parm = ParamFile('tests/test_parameters.json')
        parm.set_parameter('badParamName', 'test123')

def test_set_parameter_invalid_key_type():
    with pytest.raises(ValueError):
        parm = ParamFile('tests/test_parameters.json')
        parm.set_parameter(None, 'test123')

def test_set_parameter_change_type():
    parm = ParamFile('tests/test_parameters.json')
    new_value = 'test123'
    parm.set_parameter('adminPassword', new_value)
    assert parm.get_parameter('adminPassword') == new_value

def test_set_parameter_change_type_2():
    parm = ParamFile('tests/test_parameters.json')
    new_value = {
        "reference": {
            "keyVault": {
                "id": "/subscriptions/<subscription-id>/resourceGroups/examplegroup/providers/Microsoft.KeyVault/vaults/<vault-name>"
            },
            "secretName": "examplesecret"
        }
    }
    parm.set_parameter('adminPassword', new_value)
    assert parm.get_parameter('adminPassword') == new_value

def test_set_parameter_as_keyvault_ref():
    subscription = 'testsub'
    param = 'storageAccountType'
    secret = 'my_secret'
    kv_rg = 'my_rg'
    kv_name = 'my_kv'
    expected = {
        "reference": {
            "keyVault": {
                "id": "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.KeyVault/vaults/{}".format(subscription, kv_rg, kv_name)
            },
            "secretName": secret
        }
    }
    parm = ParamFile(src='tests/test_parameters.json', subscription=subscription)
    parm.set_parameter_as_keyvault_ref(param, secret, kv_rg, kv_name)
    assert parm.get_parameter(param) == expected

def test_set_parameter_as_keyvault_ref_bad_key():
    subscription = 'testsub'
    param = 'badparamname'
    secret = 'my_secret'
    kv_rg = 'my_rg'
    kv_name = 'my_kv'
    parm = ParamFile(src='tests/test_parameters.json', subscription=subscription)
    with pytest.raises(KeyError):
        parm.set_parameter_as_keyvault_ref(param, secret, kv_rg, kv_name)
