#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.arm_compozure.arm_file import ArmFile

class ParamFile(ArmFile):
    def __init__(self, src=None, dest=None):
        super(ParamFile, self).__init__(src, dest)

    def get_parameter(self, parameter):
        param_str = "parameters.{}".format(parameter)
        param_str_full = "{}.value".format(param_str)
        if self.key_exists(param_str_full):
            return self.get_value(param_str_full)
        elif self.key_exists(param_str):
            return self.get_value(param_str)
        else:
            raise KeyError("Parameter {} does not exist.".format(parameter))

    def set_parameter(self, parameter, value):
        new_value = {}
        new_value['value'] = value
        param_str = "parameters.{}".format(parameter)
        if self.key_exists(param_str):
            self.set_value(param_str, new_value)
        else:
            raise KeyError("Parameter {} does not exist.".format(parameter))
