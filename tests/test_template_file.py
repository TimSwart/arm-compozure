#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import config
from arm_compozure.template_file import TemplateFile

def test_init():
	test = TemplateFile('tests/test_template.json', 'test_template')
	assert hasattr(test, 'src')
	assert test.get_value('parameters.storageAccountType.defaultValue') == 'Standard_LRS'

def test_clear_tags():
	test = TemplateFile('tests/test_template.json', 'test_template')
	test.clear_tags()
	assert test.get_value('resources', 0)['tags'] == {}
