#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 15:08:05 2019

@author: michal
"""

from os import getcwd
from os.path import join

cwd = getcwd()
file2alias = { "g16Log2xyz.py" : "g16Log2xyz", "inp2scan.py" : "inp2scan",
              "lastGeom2newInput.py" : "lastGeom2newInput", "fixCoordinates.py" : "fixCoordinates" ,
              "g16Inps2NEB.py" : "g16Inps2NEB", "inp2series.py" : "inp2series"}

for script in file2alias:
    path = join(cwd, script)
    print("alias "+file2alias[script]+"='python "+path+"'")