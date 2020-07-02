#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:33:54 2020

@author: michal
"""

import sys

def amberQMMM2xyz(amberLog, xyz):
    al = open(amberLog, 'r')
    
    line  = al.readline()
    while line and not "QM Region Cartesian Coordinates" in line:
      line  = al.readline()
      
    if not line:
        print("no QM coordinates in file!")
    else:
        al.readline()
        line = al.readline()
        
        xyzLines = []
        while "QMMM:" in line:
            xyzLine = line.split()[-4:].join("   ")
            xyzLines.append(xyzLine)
            
            line = al.readline()
            
        xyzF = open(xyz, 'w')
        xyzF.write( str(len(xyzLines))+"\n\n" )
        
        for xyzLine in xyzLines:
            xyzF.write(xyzLine)
            xyzF.write("\n")
            
            
        xyzF.close()
    
    al.close()

if len(sys.argv) != 2:
    print( "Give me amber log")
else:
    amberLog = sys.argv[1] 
    xyz = amberLog.replace(".","_")+"xyz"
    amberQMMM2xyz(amberLog, xyz)