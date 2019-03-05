#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arm_file import ArmFile

class ParamFile(ArmFile):
    def __init__(self, src=None, dest=None, subscription=None):
        super(ParamFile, self).__init__(src, dest)
        self.subscription = subscription
    
    def get_parameter(self, parameter):
        if parameter is None:
            raise ValueError("Expected parameter name, recieved \'None\'.")
        param_str = "parameters.{}".format(parameter)
        param_str_full = "{}.value".format(param_str)
        if self.key_exists(param_str_full):
            return self.get_value(param_str_full)
        elif self.key_exists(param_str):
            return self.get_value(param_str)
        else:
            raise KeyError("Parameter {} does not exist.".format(parameter))

    def set_parameter(self, parameter, value):
        if parameter is None:
            raise ValueError("Expected parameter name, recieved \'None\'.")
        new_value = {}
        new_value['value'] = value
        param_str = "parameters.{}".format(parameter)
        if self.key_exists(param_str):
            self.set_value(param_str, new_value)
        else:
            raise KeyError("Parameter {} does not exist.".format(parameter))

    # set parameter by creating a Key Vault reference
    def set_parameter_as_keyvault_ref(self, parameter, secret_name, 
                                      key_vault_resource_group, key_vault_name):
        if parameter is None:
            raise ValueError("Expected parameter name, recieved \'None\'.")
        if secret_name is None or secret_name is '':
            raise ValueError("Invalid secret name.")
        if key_vault_resource_group is None:
            raise ValueError("Expected Key Vault Resource Group name, recieved \'None\'.")
        if key_vault_name is None:
            raise ValueError("Expected Key Vault name, recieved \'None\'.")
        if self.subscription is None:
            raise ValueError("Subscription name is \'None\'.")
        new_value = {
            "reference": {
                "keyVault": {
                    "id": "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.KeyVault/vaults/{}".format(self.subscription, key_vault_resource_group, key_vault_name)
                },
                "secretName": secret_name
            }
        }
        param_str = "parameters.{}".format(parameter)
        if self.key_exists(param_str):
            self.set_value(param_str, new_value)
        else:
            raise KeyError("Parameter {} does not exist.".format(parameter))