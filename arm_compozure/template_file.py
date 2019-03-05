#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arm_file import ArmFile

class TemplateFile(ArmFile):
	def __init__(self, src=None, dest=None):
		super(TemplateFile, self).__init__(src, dest)
		
	def clear_tags(self):
		self._ArmFile__data['resources'][0]['tags'] = {}

	def set_tag(self, tag_name, tag_value):
		if tag_name is None or tag_name is "":
			raise ValueError(TemplateFile.BAD_TAG_NAME)
		tags = self._ArmFile__data['resources'][0]['tags']


	class Errors(object):
		""" Store error messages
		"""
		BAD_TAG_NAME = 'Invalid tag name \'{}\' was provided.'

