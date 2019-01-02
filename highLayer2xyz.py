#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 16:09:15 2018

@author: michal
"""
import sys
from readingUtilities import isBlankLine, floatInList

def readHighLayerFromInput( oldInput ):
    oldFile = open(oldInput, 'r')
    line = oldFile.readline()
    
    #route section
    while not isBlankLine(line):
        line = oldFile.readline()
        
    line = oldFile.readline()
    #comment
    while not isBlankLine(line):
        line = oldFile.readline()
        
    line = oldFile.readline() #charges and multiplicity
    line = oldFile.readline()
    
    coords = []
    elements = []
    while not isBlankLine(line):
        
        lineSpl = line.split()
        coordInd = floatInList(lineSpl)[-3:]
        newCoords = [ float(lineSpl[c]) for c in coordInd]
        
        layerInd = lineSpl[coordInd[-1]+1]
        
        if "H" == layerInd.upper():
            coords.append(newCoords)
            element = lineSpl[0][0]
            elements.append(element)
            
        line = oldFile.readline()
    
    oldFile.close()
    
    return elements, coords

def appendCoords2File( elements, coords, file2append ):
    xyz = open(file2append, 'a')
    xyz.write(str(len(elements))+"\n\n")
    
    for el, c in zip(elements, coords):
        xyz.write(el+"\t" + str(c[0])+"\t"+str(c[1])+"\t"+str(c[2])+"\n")
        
    
    xyz.close()

if len(sys.argv) < 3:
    print(sys.argv)
    print("Potrzebuje: inputy, xyz ")
else:
    
    inputs = sys.argv[1:-1]
    xyz = sys.argv[-1]
    
    xyzF = open(xyz, 'w')
    xyzF.close()
    
    for gInput in inputs:
        el, coords = readHighLayerFromInput(gInput)
        appendCoords2File(el, coords, xyz)