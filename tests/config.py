#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this file helps resolve path issues experienced with pytest
# and must run before unit tests
# note: files in 'tests' dir run in alphabetical order, so config must
# appear above actual test files
import sys, os

file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, file_path + '/../')
sys.path.insert(1, file_path + '/../arm_compozure/')