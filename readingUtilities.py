#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:21:03 2018

@author: michal
"""

def isBlankLine(line):
    return line.isspace()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def floatInList( list2test ):
    res = []
    for i, item in enumerate(list2test):
        if isfloat(item):
            res.append(i)
    return res